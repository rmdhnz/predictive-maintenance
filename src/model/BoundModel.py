from model.BaseModel import BaseModel
import json


class BoundModel(BaseModel):
    def __init__(self, table="bounds"):
        super().__init__(table)

    def make_range(self, data, merge=False):
        range_0 = json.loads(data["range_0"])
        range_0 = list(range(range_0["start"], range_0["end"]))
        range_50 = json.loads(data["range_50"])
        range_50 = list(range(range_50["start"], range_50["end"]))
        range_100 = json.loads(data["range_100"])
        range_100 = list(range(range_100["start"], range_100["end"]))
        if merge:
            return range_0 + range_50 + range_100
        return {"range_0": range_0, "range_50": range_50, "range_100": range_100}
