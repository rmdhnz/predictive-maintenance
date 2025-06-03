import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


class Autoencoder:
    def __init__(
        self,
        hidden_layer_sizes=(3,),
        max_iter=1000,
        contamination=0.05,
        random_state=42,
    ):
        self.hidden_layer_sizes = hidden_layer_sizes
        self.max_iter = max_iter
        self.contamination = contamination
        self.random_state = random_state

        self.scaler = StandardScaler()
        self.model = MLPRegressor(
            hidden_layer_sizes=self.hidden_layer_sizes,
            max_iter=self.max_iter,
            random_state=self.random_state,
        )
        self.threshold = None

    def fit(self, X):
        # Normalisasi data
        X_scaled = self.scaler.fit_transform(X)

        self.model.fit(X_scaled, X_scaled)

        # Hitung error rekonstruksi
        X_pred = self.model.predict(X_scaled)
        mse = np.mean((X_scaled - X_pred) ** 2, axis=1)

        # Tentukan threshold anomali berdasarkan contamination
        self.threshold = np.percentile(mse, 100 * (1 - self.contamination))

        return self

    def predict(self, X):
        # Normalisasi data
        X_scaled = self.scaler.transform(X)

        # Rekonstruksi data
        X_pred = self.model.predict(X_scaled)

        # Hitung error rekonstruksi
        mse = np.mean((X_scaled - X_pred) ** 2, axis=1)

        return (mse > self.threshold).astype(int)

    def plot_results(self, X, anomalies):
        plt.figure(figsize=(8, 6))
        plt.scatter(X[:, 0], X[:, 1], c=anomalies, cmap="coolwarm", alpha=0.6)
        plt.xlabel("Current")
        plt.ylabel("Load Percent")
        plt.title("Deteksi Anomali dengan Autoencoder (MLPRegressor)")
        plt.show()
