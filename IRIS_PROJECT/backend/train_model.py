import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# =========================
# USER INPUT
# =========================
dataset_path = input("Enter dataset file (e.g. dataset_1hand.csv or dataset_2hand.csv): ")
model_name = input("Enter model name to save (e.g. asl_model.pkl or word_model.pkl): ")

# =========================
# LOAD DATASET
# =========================
data = pd.read_csv(dataset_path, header=None)

print(f"Dataset loaded: {data.shape}")

# =========================
# SPLIT FEATURES & LABELS
# =========================
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# =========================
# TRAIN-TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# TRAIN MODEL
# =========================
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# =========================
# EVALUATE MODEL
# =========================
accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy * 100:.2f}%")

# =========================
# SAVE MODEL
# =========================
with open(model_name, "wb") as f:
    pickle.dump(model, f)

print(f"Model saved as {model_name}")