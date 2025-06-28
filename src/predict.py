import pandas as pd
import numpy as np
import keras
from sklearn.preprocessing import StandardScaler
from model.TesMotorBRB3 import TesMotorBRB3
from model.TesMotorBRB7 import TesMotorBRB7
from model.TesMotorBRB37 import TesMotorBRB37
from model.TesMotorBRB77 import TesMotorBRB77
from model.TesMotor import TesMotor
from utils.Utilities import Utilities
# ============ 1. LOAD MODEL ===============
model = keras.models.load_model("model-nn/model-training-data-full.h5")
motor_model = TesMotorBRB3()
# ============ 2. BACA DATA CSV ===============
data_uji = motor_model.findAll().panda()
data_uji.drop(columns=['label_id'],inplace=True)

data_uji = Utilities.add_time_sec(data_uji)
fitur_model = ['id', 'current', 'percent_load', 'time_sec']  # <--- sesuaikan!
# Validasi kolom
for kolom in fitur_model:
    if kolom not in data_uji.columns:
        raise ValueError(f"Kolom '{kolom}' tidak ditemukan di data_uji")

# Ambil fitur yang sesuai
X_uji = data_uji[fitur_model].copy()

# Scaling (⚠️ Idealnya pakai scaler yang disimpan saat training)
scaler = StandardScaler()
X_uji_scaled = scaler.fit_transform(X_uji)

# ========== 4. Prediksi ==========
prediksi = model.predict(X_uji_scaled)
prediksi_label = np.argmax(prediksi, axis=1)

# ========== 5. Output ==========
data_uji["predicted_label_id"] = prediksi_label

print(data_uji[fitur_model + ["predicted_label_id"]].head())

# Simpan ke file
data_uji.to_csv("hasil_prediksi.csv", index=False)
print("✅ Hasil prediksi disimpan'")
