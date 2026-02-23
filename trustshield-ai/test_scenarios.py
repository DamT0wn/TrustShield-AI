#!/usr/bin/env python3
"""
TrustShield AI - Real-Life Testing Scenarios
Test the fraud detection system with realistic examples
"""

import requests
import json
from colorama import init, Fore, Style

init(autoreset=True)

API_URL = "http://127.0.0.1:8000"

# Real-life test scenarios
SCENARIOS = {
    "high_risk_scams": [
        {
            "name": "IRS Tax Scam",
            "transcript": "This is the IRS calling. You owe $5,000 in back taxes. If you don't pay immediately via wire transfer, a warrant will be issued for your arrest. You must act now to avoid legal consequences.",
            "transaction": [50000, 1, 1],  # Large amount, urgent, new recipient
            "expected_risk": "Critical"
        },
        {
            "name": "Tech Support Scam",
            "transcript": "Hello, this is Microsoft technical support. We've detected a virus on your computer. Please provide remote access and your credit card to fix this immediately. Your computer will crash if you don't act now.",
            "transaction": [2500, 1, 1],
            "expected_risk": "Critical"
        },
        {
            "name": "Grandparent Scam",
            "transcript": "Grandma, it's me! I'm in trouble and need money right away. I was in an accident and need bail money. Please don't tell mom and dad. Wire $10,000 to this account immediately.",
            "transaction": [10000, 1, 1],
            "expected_risk": "Critical"
        },
        {
            "name": "Bank Security Scam",
            "transcript": "This is your bank's fraud department. We've detected unauthorized charges. To secure your account, please verify your account number, PIN, and social security number immediately.",
            "transaction": [25000, 2, 1],
            "expected_risk": "Critical"
        },
        {
            "name": "Lottery/Prize Scam",
            "transcript": "Congratulations! You've won $1 million in the national lottery. To claim your prize, you need to pay $5,000 in processing fees and taxes upfront. Send the money today to receive your winnings.",
            "transaction": [5000, 1, 1],
            "expected_risk": "High"
        }
    ],
    "medium_risk": [
        {
            "name": "Suspicious Charity Call",
            "transcript": "Hello, we're calling from a charity for veterans. We need donations urgently. Can you provide your credit card information over the phone right now?",
            "transaction": [500, 1, 0],
            "expected_risk": "Medium"
        },
        {
            "name": "Pressure Sales Call",
            "transcript": "This is a limited time offer! You must decide now or lose this opportunity forever. We need your payment information immediately to lock in this deal.",
            "transaction": [1500, 1, 0],
            "expected_risk": "Medium"
        },
        {
            "name": "Vague Emergency",
            "transcript": "There's an urgent matter regarding your account. You need to call us back immediately at this number and provide verification details.",
            "transaction": [3000, 2, 0],
            "expected_risk": "Medium"
        }
    ],
    "low_risk_legitimate": [
        {
            "name": "Legitimate Bank Call",
            "transcript": "Hello, this is calling from your bank regarding your recent inquiry about mortgage rates. We'd like to schedule an appointment at your convenience. You can verify this call by calling the number on your bank card.",
            "transaction": [500, 1, 0],
            "expected_risk": "Low"
        },
        {
            "name": "Appointment Reminder",
            "transcript": "This is a reminder about your doctor's appointment tomorrow at 2 PM. Please call us back to confirm or reschedule if needed.",
            "transaction": [100, 1, 0],
            "expected_risk": "Low"
        },
        {
            "name": "Customer Service Follow-up",
            "transcript": "Thank you for your recent purchase. We're calling to ensure you're satisfied with your order. Is there anything we can help you with?",
            "transaction": [250, 1, 0],
            "expected_risk": "Low"
        },
        {
            "name": "Known Contact",
            "transcript": "Hi, this is Sarah from the office. Just wanted to confirm our meeting next week. Let me know if the time still works for you.",
            "transaction": [0, 0, 0],
            "expected_risk": "Low"
        }
    ]
}

def test_scenario(scenario, category):
    """Test a single scenario"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"Testing: {scenario['name']}")
    print(f"Category: {category}")
    print(f"{'='*70}{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}Transcript:{Style.RESET_ALL}")
    print(f"  {scenario['transcript'][:100]}...")
    
    print(f"\n{Fore.YELLOW}Transaction:{Style.RESET_ALL} Amount: ${scenario['transaction'][0]}, Urgency: {scenario['transaction'][1]}, New Recipient: {scenario['transaction'][2]}")
    
    try:
        # Test with the actual API (would need to modify backend to accept parameters)
        # For now, we'll use the scam classifier directly
        from ai_models.scam_classifier import predict_scam
        from ai_models.anomaly_detector import detect_anomaly
        from backend.services.risk_engine import calculate_risk
        
        # Get fraud probability from text
        fraud_prob = predict_scam(scenario['transcript'])
        
        # Get transaction anomaly flag
        import numpy as np
        trans_flag = detect_anomaly(scenario['transaction'])
        
        # Calculate final risk
        risk_score, risk_level = calculate_risk(fraud_prob, trans_flag)
        
        print(f"\n{Fore.GREEN}Results:{Style.RESET_ALL}")
        print(f"  Fraud Probability: {fraud_prob:.1%}")
        print(f"  Transaction Flag: {'⚠️  Anomaly' if trans_flag == -1 else '✓ Normal'}")
        print(f"  Risk Score: {risk_score:.1%}")
        
        # Color code the risk level
        if risk_level == "Critical":
            color = Fore.RED
            icon = "🚨"
        elif risk_level == "Medium":
            color = Fore.YELLOW
            icon = "⚠️ "
        else:
            color = Fore.GREEN
            icon = "✓"
        
        print(f"  Risk Level: {color}{icon} {risk_level}{Style.RESET_ALL}")
        print(f"  Expected: {scenario['expected_risk']}")
        
        # Check if result matches expectation
        if risk_level == scenario['expected_risk'] or \
           (scenario['expected_risk'] == "High" and risk_level == "Critical"):
            print(f"\n{Fore.GREEN}✓ Test PASSED - Detection working correctly{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}⚠ Test NOTICE - Got {risk_level}, expected {scenario['expected_risk']}{Style.RESET_ALL}")
        
        return {
            "name": scenario['name'],
            "fraud_prob": fraud_prob,
            "risk_level": risk_level,
            "expected": scenario['expected_risk']
        }
        
    except Exception as e:
        print(f"\n{Fore.RED}✗ Error: {str(e)}{Style.RESET_ALL}")
        return None

def main():
    """Run all test scenarios"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"TrustShield AI - Real-Life Scenario Testing")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    results = {
        "high_risk_scams": [],
        "medium_risk": [],
        "low_risk_legitimate": []
    }
    
    # Test high-risk scams
    print(f"\n{Fore.RED}{'='*70}")
    print(f"HIGH RISK SCAM SCENARIOS")
    print(f"{'='*70}{Style.RESET_ALL}")
    for scenario in SCENARIOS["high_risk_scams"]:
        result = test_scenario(scenario, "High Risk Scam")
        if result:
            results["high_risk_scams"].append(result)
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    # Test medium risk
    print(f"\n{Fore.YELLOW}{'='*70}")
    print(f"MEDIUM RISK SCENARIOS")
    print(f"{'='*70}{Style.RESET_ALL}")
    for scenario in SCENARIOS["medium_risk"]:
        result = test_scenario(scenario, "Medium Risk")
        if result:
            results["medium_risk"].append(result)
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    # Test legitimate calls
    print(f"\n{Fore.GREEN}{'='*70}")
    print(f"LOW RISK LEGITIMATE SCENARIOS")
    print(f"{'='*70}{Style.RESET_ALL}")
    for scenario in SCENARIOS["low_risk_legitimate"]:
        result = test_scenario(scenario, "Low Risk Legitimate")
        if result:
            results["low_risk_legitimate"].append(result)
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    # Summary
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"TEST SUMMARY")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    total_tests = sum(len(v) for v in results.values())
    print(f"Total Scenarios Tested: {total_tests}")
    
    print(f"\n{Fore.RED}High Risk Scams:{Style.RESET_ALL}")
    for r in results["high_risk_scams"]:
        print(f"  • {r['name']}: {r['fraud_prob']:.1%} fraud probability → {r['risk_level']}")
    
    print(f"\n{Fore.YELLOW}Medium Risk:{Style.RESET_ALL}")
    for r in results["medium_risk"]:
        print(f"  • {r['name']}: {r['fraud_prob']:.1%} fraud probability → {r['risk_level']}")
    
    print(f"\n{Fore.GREEN}Legitimate Calls:{Style.RESET_ALL}")
    for r in results["low_risk_legitimate"]:
        print(f"  • {r['name']}: {r['fraud_prob']:.1%} fraud probability → {r['risk_level']}")
    
    print(f"\n{Fore.CYAN}Testing complete!{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
