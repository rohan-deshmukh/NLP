# import libraries
import gensim
import os
from nltk.tokenize import ToktokTokenizer

model_dir = os.path.dirname(os.path.abspath(__file__)) + '/gensim_model'


class Model(object):

    def __init__(self):
        self.toko_toknizer = ToktokTokenizer()

    def train_similarity(self, train_q_list):

        global dictionary, tf_idf_obj, gensim_similarity_obj

        # work tokenization using toktoktokenizer
        tokenized_q_list = [[w.lower() for w in self.toko_toknizer.tokenize(text)] for text in train_q_list]

        # dictionary mapping each word to an integer
        dictionary = gensim.corpora.Dictionary(tokenized_q_list)

        # list of list - each inner list consists of tuples mapping each word to the number of times it appeared in a
        # single doc
        bagofwords_corpus = [dictionary.doc2bow(token) for token in tokenized_q_list]

        # td-idf object
        tf_idf_obj = gensim.models.TfidfModel(bagofwords_corpus)

        # similarity object
        gensim_similarity_obj = gensim.similarities.Similarity(model_dir,
                                                               tf_idf_obj[bagofwords_corpus],
                                                               num_features=len(dictionary))

    def test_similarity(self, test_q):
        # test new document - similarity score list
        new_q_tokonize = [w.lower() for w in self.toko_toknizer.tokenize(test_q)]
        new_q_dictionary = dictionary.doc2bow(new_q_tokonize)
        new_q_tf_idf = tf_idf_obj[new_q_dictionary]
        similarity_score_list = gensim_similarity_obj[new_q_tf_idf].tolist()

        # similar sentence index
        max_similar_score = max(similarity_score_list)
        most_similar_doc_index = similarity_score_list.index(max_similar_score)
        return most_similar_doc_index, float(max_similar_score)

    @staticmethod
    def json_response(qa_dict, prev_list, new_list, model_obj):
        answered_dict = {}
        for question in new_list:
            most_similar_q_index, score = model_obj.test_similarity(question)
            similar_q = prev_list[most_similar_q_index]

            # Response to new question - json
            new_response = qa_dict[str(similar_q)]
            answered_dict.update({str(question): [str(new_response), str(similar_q)]})
        return answered_dict

    @staticmethod
    def excel_response(qa_dict, prev_list, new_list, model_obj):
        answered_list = []
        for question in new_list:
            most_similar_q_index, score = model_obj.test_similarity(question)
            similar_q = prev_list[most_similar_q_index]

            # Response to new question
            new_response = qa_dict[str(similar_q)]
            answered_list.append([str(question), str(new_response), str(similar_q), round(score, 2)])
        return answered_list
