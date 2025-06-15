from model.BaseModel import BaseModel


class MotorModel(BaseModel):
    def __init__(self, table="motor_current"):
        super().__init__(table)
