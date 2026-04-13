import numpy as np
import pickle

model = pickle.load(open("digits_model.pkl", "rb"))

X = np.load("X.npy")
Y = np.load("Y.npy")

# flatten images
X = X.reshape(X.shape[0], -1)

# predict
prediction = model.predict([X[0]])

# convert one-hot → number
pred_digit = np.argmax(prediction)
actual_digit = np.argmax(Y[0])

print("Predicted:", pred_digit)
print("Actual:", actual_digit)