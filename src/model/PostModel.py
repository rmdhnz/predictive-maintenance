from src.model.BaseModel import BaseModel

class PostModel(BaseModel) : 
  def __init__(self, table):
    super().__init__(table)