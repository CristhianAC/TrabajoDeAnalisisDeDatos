import pandas as pd
import os
class DictCreator:
    def __init__(self):
        script_directory = os.path.dirname(__file__)
        parent_directory = os.path.abspath(os.path.join(script_directory, os.pardir))
        df = pd.read_excel(parent_directory + "/Excel/Educación Sexual.xlsx")
        dic = df.to_dict()
        keys = list(dic.keys())
        for key in keys:
            dic[key] = list(dic[key].values())
        self.dict = dic

