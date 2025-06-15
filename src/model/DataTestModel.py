from model.BaseModel import BaseModel


class DataTestModel(BaseModel):
    def __init__(self, table="data_test"):
        super().__init__(table)
