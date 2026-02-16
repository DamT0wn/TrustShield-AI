import numpy as np
from sklearn.ensemble import IsolationForest

transactions = np.array([
    [500, 1, 0],
    [700, 2, 0],
    [50000, 5, 1],
    [100000, 8, 1]
])

model = IsolationForest(contamination=0.2)

model.fit(transactions)

def detect_anomaly(transaction):

    pred = model.predict([transaction])

    return int(pred[0])