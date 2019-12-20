import pandas as pd
import glob


class ExcelData(object):

    def __init__(self, excel_path):
        self.path = ''.join([excel_path, '*.xlsx'])

    def get_qa(self):
        qadict = {}
        for filepath in glob.glob(self.path):
            if filepath.endswith(".xlsx"):
                df = pd.read_excel(filepath, header=0)
                df = df.dropna(axis=1, how='all').dropna(axis=0, how='all')

                dictionary = {'\xa0': ''}
                df.replace(dictionary, regex=True, inplace=True)

                temp_dict = df.set_index('Question')['Response'].to_dict()
                qadict.update(temp_dict)
        qlist = list(qadict)

        return qadict, qlist

    def get_q(self):
        for filepath in glob.glob(self.path):
            if filepath.endswith(".xlsx"):
                df = pd.read_excel(filepath, header=0)
                df = df.dropna(axis=1, how='all').dropna(axis=0, how='all')

                dictionary = {'\xa0': ''}
                df.replace(dictionary, regex=True, inplace=True)

        new_q_list = df['Question'].tolist()
        return new_q_list

