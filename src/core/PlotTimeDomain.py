from model.MotorModel import MotorModel
from model.TesMotor import TesMotor
from model.MotorBRB3mm import MotorBRB3mm
from model.MotorBRB7mm import MotorBRB7mm
from utils.Utilities import Utilities


class PlotTimeDomain:
    def run(self):
        motor_model = TesMotor()
        data_normal = motor_model.findAll().panda()
        print(data_normal)
        Utilities.plot_time_domain(data_normal, subplot=True)
