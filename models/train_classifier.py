import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

import pickle

# Load dataset
data = pd.read_csv("data/tickets.csv")

# Features and labels
X = data["complaint"]
y = data["category"]

# Convert text into numbers
vectorizer = TfidfVectorizer()

X_vectorized = vectorizer.fit_transform(X)

# Train model
model = LogisticRegression()

model.fit(X_vectorized, y)

# Save model
with open("models/classifier.pkl", "wb") as f:
    pickle.dump(model, f)

# Save vectorizer
with open("models/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Model trained successfully!")