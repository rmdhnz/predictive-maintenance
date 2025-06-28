from model.MotorModel import MotorModel
from model.MotorBRB3mm import MotorBRB3mm
from model.MotorBRB7mm import MotorBRB7mm
from model.TesMotor import TesMotor
from model.TesMotorBRB3 import TesMotorBRB3
from model.TesMotorBRB7 import TesMotorBRB7
from model.TesMotorBRB37 import TesMotorBRB37

from model.TesMotorBRB77 import TesMotorBRB77
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.Utilities import Utilities

model_data = [TesMotor,TesMotorBRB3,TesMotorBRB7,TesMotorBRB37,TesMotorBRB77]
for model in model_data : 
    md = model()
    data = md.findAll().panda()
    df_data = Utilities.fft_current_by_load(data,label=0)
    # print(df_data)
    loads = data["percent_load"].unique()
    Nr_dict = {0: 1490, 50: 1440, 100: 1390}
    records = []
    for load in loads : 
        df_load = df_data[df_data["percent_load"]==load].copy()
        freq = df_load["frequency"].values
        amp = df_load["current_magnitude"].values
        rec = Utilities.sideband_amplitudes(Nr_dict, freq, amp, load)
        records.append(rec)

    result = pd.DataFrame(records)
    print("\nHasil side-band & amplitudo:")
    print(result)
