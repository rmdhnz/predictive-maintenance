from model.BaseModel import BaseModel


class MotorBRB7mm(BaseModel):
    def __init__(self, table="motor_brb_current_7mm"):
        super().__init__(table)
