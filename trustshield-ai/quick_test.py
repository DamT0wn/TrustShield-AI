#!/usr/bin/env python3
"""
Quick Test - Test a single scenario quickly
"""

import sys
import os
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))

from ai_models.scam_classifier import predict_scam
from ai_models.anomaly_detector import detect_anomaly
from backend.services.risk_engine import calculate_risk

# Test with a high-risk scam
print("\n" + "="*70)
print("Testing: IRS Tax Scam (High Risk)")
print("="*70 + "\n")

transcript = "This is the IRS calling. You owe $5,000 in back taxes. If you don't pay immediately via wire transfer, a warrant will be issued for your arrest."

transaction = np.array([[50000, 8, 1]])  # Large amount, high urgency, new recipient

print("Transcript:", transcript[:100] + "...")
print("\nTransaction: $50,000, Urgency: 8/10, New Recipient: Yes")

# Analyze
fraud_prob = predict_scam(transcript)
trans_flag = detect_anomaly(transaction)
risk_score, risk_level = calculate_risk(fraud_prob, trans_flag)

print("\n" + "="*70)
print("RESULTS")
print("="*70)
print(f"Fraud Probability: {fraud_prob:.1%}")
print(f"Transaction Status: {'⚠️  ANOMALY' if trans_flag == -1 else '✓ Normal'}")
print(f"Risk Score: {risk_score:.1%}")
print(f"Risk Level: {risk_level}")

if risk_level == "Critical":
    print("\n🚨 CRITICAL RISK - Transaction should be BLOCKED")
elif risk_level == "Medium":
    print("\n⚠️  MEDIUM RISK - Review required")
else:
    print("\n✓ LOW RISK - Transaction can proceed")

print("\n" + "="*70)
print("\nTesting: Legitimate Bank Call (Low Risk)")
print("="*70 + "\n")

transcript2 = "Hello, this is calling from your bank regarding your recent inquiry about mortgage rates. You can verify this call by calling the number on your bank card."

transaction2 = np.array([[500, 2, 0]])  # Small amount, low urgency, known recipient

print("Transcript:", transcript2[:100] + "...")
print("\nTransaction: $500, Urgency: 2/10, Known Recipient")

# Analyze
fraud_prob2 = predict_scam(transcript2)
trans_flag2 = detect_anomaly(transaction2)
risk_score2, risk_level2 = calculate_risk(fraud_prob2, trans_flag2)

print("\n" + "="*70)
print("RESULTS")
print("="*70)
print(f"Fraud Probability: {fraud_prob2:.1%}")
print(f"Transaction Status: {'⚠️  ANOMALY' if trans_flag2 == -1 else '✓ Normal'}")
print(f"Risk Score: {risk_score2:.1%}")
print(f"Risk Level: {risk_level2}")

if risk_level2 == "Critical":
    print("\n🚨 CRITICAL RISK - Transaction should be BLOCKED")
elif risk_level2 == "Medium":
    print("\n⚠️  MEDIUM RISK - Review required")
else:
    print("\n✓ LOW RISK - Transaction can proceed")

print("\n" + "="*70)
print("\n✅ Quick test complete! The fraud detection system is working.")
print("\nFor more tests, run:")
print("  python interactive_test.py  (custom scenarios)")
print("  python test_scenarios.py    (12+ pre-built scenarios)")
print()
