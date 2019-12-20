
# @TODO: Need to fix this - universal model pooling module

import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import ToktokTokenizer
from nltk.tokenize import word_tokenize
from gensim.similarities import Similarity
from gensim.models import TfidfModel
from nltk.corpus import stopwords


class Models(object):
    def __init__(self, question_list):
        self.q_list = question_list

    def d2v_model(self):
        tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(self)]

        max_epochs = 100
        vec_size = 20
        alpha = 0.025

        model = Doc2Vec(vector_size=vec_size,
                        alpha=alpha,
                        min_alpha=0.00025,
                        min_count=1,
                        dm=1)

        model.build_vocab(tagged_data)

        for epoch in range(max_epochs):
            model.train(tagged_data,
                        total_examples=model.corpus_count,
                        epochs=model.iter)
            model.alpha -= 0.0002
            model.min_alpha = model.alpha

        model.save("/Users/rdeshmukh003/Desktop/Rohan/Xoro/xoro-demo/models/d2v.bin")

    def gensim_tdidf_model(self):

        query_docs = [[w.lower() for w in word_tokenize(text)] for text in self]
        dictionary = gensim.corpora.Dictionary(query_docs)
        corpus = [dictionary.doc2bow(gen_doc) for gen_doc in query_docs]
        tf_idf = TfidfModel(corpus)
        gensim_model = Similarity('/Users/rdeshmukh003/Desktop/Rohan/Xoro/xoro-demo/models', tf_idf[corpus], num_features=len(dictionary))

        return query_docs, dictionary, corpus, tf_idf, gensim_model


class Preprocessing(object):
    def __init__(self, input_line):
        self.input = input_line.lower()

        stop_words = set(stopwords.words('english'))
        word_tokens = ToktokTokenizer().tokenize(self)

        tokenized_input = [w for w in word_tokens if w not in stop_words]
        return tokenized_input


class CalcSimilarity(object):
    def __init__(self, model, q_list, q_test):
        self.model = model
        self.q_list = q_list
        self.new_q = q_test

    def d2v_calc_sim(self):
        similar_docs = self.model.docvecs.most_similar(positive=[self.model.infer_vector(self.new_q)])
        return similar_docs

    # d2v
    d2v_model = Doc2Vec.load("/Users/rdeshmukh003/Desktop/Rohan/Xoro/xoro-demo/models/d2v.bin")
    gensim_model = model_obj.gensim_tdidf_model()

    new_q = "Please describe all entity applications that are made with McDonald's applications.".split(" ")
    similarity_obj = all_models.CalcSimilarity(new_q)

    similar_docs = d2v_model.docvecs.most_similar(positive=[d2v_model.infer_vector(new_q)])
    print(similar_docs)

    def gensim_calc_sim(self,dictionary, tf_idf, gensim_model):
        query_docs = [[w.lower() for w in word_tokenize(text)] for text in self.new_q]
        query_doc_bow = dictionary.doc2bow(query_docs)
        query_doc_tf_idf = tf_idf[query_doc_bow]
        similarity_score_list = gensim_model[query_doc_tf_idf].tolist()

        most_similar_doc_index = similarity_score_list.index(max(similarity_score_list))
        print(most_similar_doc_index)
        print(self.q_list[most_similar_doc_index])
        a_to_q = self.q_list[str(self.q_list[most_similar_doc_index])]
        print(a_to_q)