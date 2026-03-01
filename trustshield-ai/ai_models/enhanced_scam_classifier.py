"""
Enhanced Scam Classifier with improved pattern detection and confidence scoring.
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import re

class EnhancedScamClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            ngram_range=(1, 3),
            min_df=1
        )
        self.model = LogisticRegression(max_iter=1000, random_state=42)
        self.scam_keywords = [
            'urgent', 'verify', 'suspended', 'frozen', 'immediately',
            'account', 'security', 'pin', 'password', 'ssn', 'social security',
            'irs', 'tax', 'arrest', 'warrant', 'legal action', 'customs',
            'prize', 'lottery', 'won', 'claim', 'grant', 'investment',
            'microsoft', 'tech support', 'virus', 'remote access',
            'cvv', 'credit card', 'bank details', 'wire transfer',
            'grandson', 'emergency', 'trouble', 'help', 'money',
            'act now', 'limited time', 'expire', 'final notice'
        ]
        self.trained = False
    
    def train(self, csv_path="datasets/enhanced_scam_texts.csv"):
        """Train the classifier on the dataset."""
        try:
            data = pd.read_csv(csv_path)
        except FileNotFoundError:
            # Fallback to original dataset
            data = pd.read_csv("datasets/scam_texts.csv")
        
        X = self.vectorizer.fit_transform(data["text"])
        y = data["label"]
        
        self.model.fit(X, y)
        self.trained = True
        
        return len(data)
    
    def extract_features(self, text):
        """Extract additional features from text."""
        text_lower = text.lower()
        
        features = {
            'keyword_count': sum(1 for kw in self.scam_keywords if kw in text_lower),
            'urgency_words': sum(1 for word in ['urgent', 'immediately', 'now', 'asap'] if word in text_lower),
            'request_info': sum(1 for word in ['pin', 'password', 'ssn', 'account', 'cvv'] if word in text_lower),
            'threat_words': sum(1 for word in ['arrest', 'frozen', 'suspended', 'legal'] if word in text_lower),
            'has_numbers': 1 if re.search(r'\d', text) else 0,
            'length': len(text.split())
        }
        
        return features
    
    def predict_scam(self, text):
        """
        Predict scam probability with enhanced confidence scoring.
        Returns: (probability, confidence, risk_factors)
        """
        if not self.trained:
            self.train()
        
        # Get ML model prediction
        X_test = self.vectorizer.transform([text])
        ml_prob = self.model.predict_proba(X_test)[0][1]
        
        # Extract additional features
        features = self.extract_features(text)
        
        # Calculate feature-based score
        feature_score = min(1.0, (
            features['keyword_count'] * 0.05 +
            features['urgency_words'] * 0.15 +
            features['request_info'] * 0.20 +
            features['threat_words'] * 0.15
        ))
        
        # Combine scores (weighted average)
        final_prob = (ml_prob * 0.7) + (feature_score * 0.3)
        
        # Calculate confidence based on feature strength
        confidence = min(0.95, 0.5 + (features['keyword_count'] * 0.05))
        
        # Identify risk factors
        risk_factors = []
        if features['urgency_words'] > 0:
            risk_factors.append("Urgency language detected")
        if features['request_info'] > 0:
            risk_factors.append("Requesting sensitive information")
        if features['threat_words'] > 0:
            risk_factors.append("Threatening language detected")
        if features['keyword_count'] >= 3:
            risk_factors.append("Multiple scam keywords present")
        
        return final_prob, confidence, risk_factors

# Global instance
classifier = EnhancedScamClassifier()

def predict_scam(text):
    """Backward compatible function."""
    prob, _, _ = classifier.predict_scam(text)
    return prob

def predict_scam_detailed(text):
    """Enhanced function with detailed analysis."""
    return classifier.predict_scam(text)
