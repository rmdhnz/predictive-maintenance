from model.BaseModel import BaseModel


class MotorDBModel(BaseModel):
    def __init__(self, table="motor_db"):
        super().__init__(table)
