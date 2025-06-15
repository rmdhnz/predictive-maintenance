from model.BaseModel import BaseModel


class MotorBRB3mm(BaseModel):
    def __init__(self, table="motor_brb_current_3mm"):
        super().__init__(table)
