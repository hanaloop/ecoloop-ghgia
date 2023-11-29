import pandas as pd


def return_list(func):
    def inner(self, data: pd.DataFrame):
        if type(data) != pd.DataFrame:
            return func(self, data)
        return func(self,data = data.to_dict(orient='records'))
    return inner
    
        