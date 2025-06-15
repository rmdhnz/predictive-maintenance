#!/usr/bin/env python3
from sklearn.utils import resample
from model import TesMotorBRB3, TesMotorBRB7
from model.MotorBRB7mm import MotorBRB7mm
from model.MotorModel import MotorModel
from model.MotorBRB3mm import MotorBRB3mm
from model.MotorBRB3_7_mm import MotorBRB3_7_mm
from model.TesMotor import TesMotor
from utils.Utilities import Utilities
from utils.MotorFaultNN import MotorFaultNN
import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score


def app():
    motor_normal = MotorModel()
    motor_brb_3 =   MotorBRB3mm()
    motor_brb_7 = MotorBRB7mm()
    # motor_brb_3_7 = TesMotorBRB37()
    # motor_brb_7_7 = TesMotorBRB77()

    print("Load Data...")

    data_normal = motor_normal.findAll().panda()
    data_brb_3 = motor_brb_3.findAll().panda()
    data_brb_7 = motor_brb_7.findAll().panda()
    # data_brb_3_7 = motor_brb_3_7.findAll().panda()
    # data_brb_7_7 = motor_brb_7_7.findAll().panda()
    print("DONE!")
    print("MERGE DATA...")
    data_normal = Utilities.add_time_sec(data_normal, replace=True)
    data_brb_3 = Utilities.add_time_sec(data_brb_3, replace=True)
    data_brb_7 = Utilities.add_time_sec(data_brb_7, replace=True)
    df_full = pd.concat([data_normal, data_brb_3, data_brb_7], ignore_index=True)
    print(df_full)

    # print("fft transform...")
    # df_normal = Utilities.fft_current_db_by_load(data_normal, label=0)
    # df_brb_3 = Utilities.fft_current_db_by_load(data_brb_3, label=1)
    # df_brb_7 = Utilities.fft_current_db_by_load(data_brb_7, label=2)
    # df_brb_3_7 = Utilities.fft_current_db_by_load(data_brb_3_7, label=3)
    # df_brb_7_7 = Utilities.fft_current_db_by_load(data_brb_7_7, label=4)

    # min_size = min(len(df_normal), len(df_brb_3), len(df_brb_7))

    # df_0_bal = resample(df_normal, replace=False, n_samples=min_size, random_state=42)
    # df_1_bal = resample(df_brb_3, replace=False, n_samples=min_size, random_state=42)
    # df_2_bal = resample(df_brb_7, replace=False, n_samples=min_size, random_state=42)

    # print("DONE!")

    # print("MERGE FFT DATA...")
    # df_full = pd.concat([df_0_bal, df_1_bal, df_2_bal], ignore_index=True)

    print("DONE!")

    print("PREPROCESSING...")

    # Asumsi df_full sudah berisi data lengkap yang mencakup kolom fitur dan label
    X = df_full.drop(columns=["label_id"])  # fitur
    y = df_full["label_id"]  # label kerusakan

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42
    )

    # Convert ke tensor untuk PyTorch
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train.values, dtype=torch.long)
    y_test_tensor = torch.tensor(y_test.values, dtype=torch.long)

    # Tentukan dimensi input dan output
    input_dim = X_train.shape[1]  # Jumlah fitur
    output_dim = len(y.unique())  # Jumlah kelas (5 jenis kerusakan)

    print("DONE!")

    print("MODELLING NN...")

    # Buat model
    model = MotorFaultNN(input_dim=input_dim, output_dim=output_dim)

    # Loss function dan optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Training loopcha
    epochs = 50
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()

        # Forward pass
        outputs = model(X_train_tensor)

        # Calculate loss
        loss = criterion(outputs, y_train_tensor)

        # Backward pass
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")

        # Print loss per epoch
        # if (epoch + 1) % 10 == 0:
        #     print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")

    model.eval()
    with torch.no_grad():
        y_pred = model(X_test_tensor).argmax(
            dim=1
        )  # Ambil label dengan probabilitas tertinggi
        accuracy = accuracy_score(y_test_tensor, y_pred)
        report = classification_report(y_test_tensor, y_pred, output_dict=True)

    print(f"Accuracy: {accuracy*100:.2f}%")
    print("\nClassification Report:")
    print(report)

    print("Save Model...")
    # Simpan model
    torch.save(model.state_dict(), "model-nn/1_model_training_time_domain.pth")
