import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

data = pd.read_csv("datasets/scam_texts.csv")

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(data["text"])

y = data["label"]

model = LogisticRegression()

model.fit(X, y)

def predict_scam(text):

    X_test = vectorizer.transform([text])

    prob = model.predict_proba(X_test)[0][1]

    return prob