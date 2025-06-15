import pandas as pd


class ResultWrapper:
    def __init__(self, data, description, base_model):
        self.data = data
        self.description = description
        self.base_model = base_model

    def panda(self):
        columns = [desc[0] for desc in self.description]
        df = pd.DataFrame(self.data, columns=columns)
        self.base_model.close()
        return df

    def list(self):
        self.base_model.close()
        return self.data

    def first(self):
        self.base_model.close()
        if self.data:
            return self.data[0]
        return None
