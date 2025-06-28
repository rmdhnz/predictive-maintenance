from model.MotorModel import MotorModel
from model.MotorBRB3mm import MotorBRB3mm
from model.MotorBRB7mm import MotorBRB7mm
from model.TesMotor import TesMotor
from model.TesMotorBRB3 import TesMotorBRB3
from model.TesMotorBRB7 import TesMotorBRB7
from model.TesMotorBRB37 import TesMotorBRB37
from model.TesMotorBRB77 import TesMotorBRB77
from model.MotorModel import MotorModel
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def rms(data) :
    return np.sqrt(np.mean(np.square(data)))

list_model = [TesMotor,TesMotorBRB3,TesMotorBRB7,TesMotorBRB37,TesMotorBRB77]
for model in list_model: 
    motor_model = model()
    data = motor_model.findAll().panda()

    rms_table = (
        data.groupby(["percent_load", "label_id"])["current"]
        .apply(rms)            
        .unstack("label_id")      
        .sort_index()          
    )
    print("\nTabel RMS arus (ampere)\n")
    print(rms_table.round(3))  
