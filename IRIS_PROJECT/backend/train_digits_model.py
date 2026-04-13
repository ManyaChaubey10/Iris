import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

X = np.load("X.npy")
Y = np.load("Y.npy")

X = X.reshape(X.shape[0], -1)

model = RandomForestClassifier()
model.fit(X, Y)

pickle.dump(model, open("digits_model.pkl", "wb"))

print("Model trained successfully!")