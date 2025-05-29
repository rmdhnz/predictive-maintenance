#!/usr/bin/env python3

from src.model.MotorModel import MotorModel
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt


def labeled(df, path=None):
    # 2. Buat dua DataFrame: normal (label 0) dan fault (label 1)
    df_normal = pd.DataFrame({"current": df["current_normal"], "label": 0})

    df_fault = pd.DataFrame({"current": df["current_fault"], "label": 1})

    # 3. Gabungkan data
    df_labeled = pd.concat([df_normal, df_fault], ignore_index=True)

    # 4. (Opsional) Hapus NaN jika ada
    df_labeled.dropna(inplace=True)

    # 5. Simpan ke file baru (opsional)
    if not path:
        df_labeled.to_csv("data_motor_labeled.csv", index=False)
    return df_labeled


def app():
    # 1. Load file CSV
    df = pd.read_csv("data/simulated_motor_data.csv")
    df = labeled(df)

    X = df[["current"]].values
    y = df["label"].values

    # 3. Normalisasi data arus (fitur tunggal)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 4. Split data latih dan data uji
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    # 5. Buat model Neural Network
    model = MLPClassifier(
        hidden_layer_sizes=(8,),  # 1 hidden layer, 8 neuron
        activation="relu",
        solver="adam",
        max_iter=500,
        random_state=42,
    )

    # 6. Training model
    model.fit(X_train, y_train)

    # 7. Prediksi dan evaluasi
    y_pred = model.predict(X_test)
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # 8. Visualisasi hasil klasifikasi
    plt.figure(figsize=(8, 5))
    plt.scatter(X_test, y_test, label="True Label", marker="o", alpha=0.6)
    plt.scatter(X_test, y_pred, label="Predicted Label", marker="x", alpha=0.6)
    plt.xlabel("Arus Motor (distandardisasi)")
    plt.ylabel("Label (0: Normal, 1: Fault)")
    plt.title("Prediksi Neural Network berdasarkan Arus")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
