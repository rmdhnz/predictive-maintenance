import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import tensorflow as tf
from keras import layers, models
import matplotlib.pyplot as plt
# ===================
# 1. Load Data
# ===================
from model import TesMotorBRB3, TesMotorBRB7
from model.MotorBRB7mm import MotorBRB7mm
from model.MotorModel import MotorModel
from model.MotorBRB3mm import MotorBRB3mm
from model.MotorBRB3_7_mm import MotorBRB3_7_mm
from model.MotorBRB7_7_mm import MotorBRB7_7_mm
from model.TesMotor import TesMotor
from utils.Utilities import Utilities

motor_normal = MotorModel()
motor_brb_3 = MotorBRB3mm()
motor_brb_7 = MotorBRB7mm()
motor_brb_37 = MotorBRB3_7_mm()
motor_brb_77 = MotorBRB7_7_mm()

print("Load Data...")
data_normal = motor_normal.findAll().panda()
data_brb_3 = motor_brb_3.findAll().panda()
data_brb_7 = motor_brb_7.findAll().panda()
data_brb_37 = motor_brb_37.findAll().panda()
data_brb_77= motor_brb_77.findAll().panda()
print("DONE!")

print("MERGE DATA...")
data_normal = Utilities.add_time_sec(data_normal, replace=True)
data_brb_3 = Utilities.add_time_sec(data_brb_3, replace=True)
data_brb_7 = Utilities.add_time_sec(data_brb_7, replace=True)
data_brb_37 = Utilities.add_time_sec(data_brb_37, replace=True)
data_brb_77 = Utilities.add_time_sec(data_brb_77, replace=True)
df_full = pd.concat([data_normal, data_brb_3, data_brb_7,data_brb_37,data_brb_77], ignore_index=True)
print(df_full)

print("PREPROCESSING...")
X = df_full.drop(columns=["label_id"])
y = df_full["label_id"]

print(X)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

print("MODELLING NN...")
input_dim = X_train.shape[1]
print("Inout dimension : ",input_dim)

output_dim = len(np.unique(y))

model = models.Sequential([
    layers.Dense(64, activation='sigmoid', input_shape=(input_dim,)),
    layers.Dense(32, activation='sigmoid'),
    layers.Dense(output_dim, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

history = model.fit(X_train, y_train, epochs=15, batch_size=32, verbose=1)
# Ambil data dari history
train_loss = history.history['loss']
epochs = range(1, len(train_loss) + 1)

# Plot Loss
plt.figure(figsize=(8, 5))
plt.plot(epochs, train_loss, 'b-', label='Train Loss')

# Jika kamu punya data validasi:
if 'val_loss' in history.history:
    val_loss = history.history['val_loss']
    plt.plot(epochs, val_loss, 'g-', label='Validation Loss')

# Evaluasi test loss, bisa ditampilkan juga sebagai garis horizontal
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
plt.axhline(y=loss, color='r', linestyle='-', label='Test Loss')

# Titik best validation
if 'val_loss' in history.history:
    best_epoch = np.argmin(val_loss) + 1
    best_val = min(val_loss)
    plt.scatter(best_epoch, best_val, s=100, color='green', edgecolor='black', label='Best')

plt.title(f'Best Validation Performance is {best_val:.7f} at epoch {best_epoch}')
plt.xlabel('Epochs')
plt.ylabel('Mean Squared Error (MSE)')
plt.yscale('log')  # Gunakan log scale untuk meniru grafik MATLAB
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
print("EVALUATION...")
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
y_pred = np.argmax(model.predict(X_test), axis=1)

print(f"Accuracy: {accuracy*100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("Save Model...")
model.save("model-nn/3-model-training-data-full.h5")
