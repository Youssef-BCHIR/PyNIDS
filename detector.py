import numpy as np
import pickle
import os
from sklearn.ensemble import IsolationForest

MODEL_PATH = "pynids_model.pkl"

class Detector:

    def __init__(self, contamination=0.05):
        self.model = IsolationForest(
            contamination = contamination,
            random_state = 42,
            n_estimators = 100
        )
        self.is_trained = False
        self.training_data = []

    def add_training_sample(self, feature_vector):
        self.training_data.append(feature_vector)
    
    def train(self):
        if len(self.training_data) < 400:
            print("[!] Not enough training data yet.")
            return False
        X = np.array(self.training_data)
        self.model.fit(X)
        self.is_trained = True
        print(f"[*] Model trained on {len(self.training_data)} samples.")
        return True

    def predict(self, feature_vector):
        if not self.is_trained:
            return None

        X = np.array([feature_vector])
        prediction = self.model.predict(X)[0]
        score=self.model.score_samples(X)[0]

        return {
            "is_anomaly": prediction == -1,
            "score": score,
            "prediction": prediction
        }

    def save(self):
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(self.model, f)
        print(f"[*] Model saved to {MODEL_PATH}")
        
    def load(self):
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)
            self.is_trained = True
            print(f"[*] Model loaded from {MODEL_PATH}")
            return True
        return False
    