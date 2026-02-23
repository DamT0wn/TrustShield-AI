#!/usr/bin/env python3
"""
TrustShield AI - Interactive Testing Tool
Test with your own custom scenarios in real-time
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from ai_models.scam_classifier import predict_scam
from ai_models.anomaly_detector import detect_anomaly
from backend.services.risk_engine import calculate_risk
from colorama import init, Fore, Style

init(autoreset=True)

def print_header():
    """Print application header"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"TrustShield AI - Interactive Testing Tool")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    print("Test fraud detection with your own scenarios")
    print("Type 'quit' or 'exit' to stop\n")

def get_transcript():
    """Get call transcript from user"""
    print(f"{Fore.YELLOW}Enter the call transcript:{Style.RESET_ALL}")
    print("(What did the caller say?)")
    transcript = input("> ").strip()
    return transcript

def get_transaction():
    """Get transaction details from user"""
    print(f"\n{Fore.YELLOW}Transaction Details:{Style.RESET_ALL}")
    
    try:
        amount = float(input("Amount ($): ").strip() or "0")
        urgency = int(input("Urgency level (0-10): ").strip() or "0")
        new_recipient = int(input("New recipient? (0=No, 1=Yes): ").strip() or "0")
        return [amount, urgency, new_recipient]
    except ValueError:
        print(f"{Fore.RED}Invalid input, using defaults{Style.RESET_ALL}")
        return [0, 0, 0]

def analyze_scenario(transcript, transaction):
    """Analyze the scenario and display results"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print("ANALYZING...")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    try:
        # Get fraud probability
        fraud_prob = predict_scam(transcript)
        
        # Get transaction anomaly
        import numpy as np
        trans_flag = detect_anomaly(transaction)
        
        # Calculate final risk
        risk_score, risk_level = calculate_risk(fraud_prob, trans_flag)
        
        # Display results
        print(f"{Fore.GREEN}ANALYSIS RESULTS:{Style.RESET_ALL}\n")
        
        print(f"📝 Transcript Analysis:")
        print(f"   Fraud Probability: {fraud_prob:.1%}")
        if fraud_prob > 0.7:
            print(f"   {Fore.RED}⚠️  HIGH FRAUD INDICATORS DETECTED{Style.RESET_ALL}")
        elif fraud_prob > 0.4:
            print(f"   {Fore.YELLOW}⚠️  MODERATE FRAUD INDICATORS{Style.RESET_ALL}")
        else:
            print(f"   {Fore.GREEN}✓ Low fraud indicators{Style.RESET_ALL}")
        
        print(f"\n💰 Transaction Analysis:")
        print(f"   Amount: ${transaction[0]:,.2f}")
        print(f"   Urgency: {transaction[1]}/10")
        print(f"   New Recipient: {'Yes' if transaction[2] == 1 else 'No'}")
        print(f"   Status: {Fore.RED + '⚠️  ANOMALY DETECTED' if trans_flag == -1 else Fore.GREEN + '✓ Normal pattern'}{Style.RESET_ALL}")
        
        print(f"\n🎯 Final Risk Assessment:")
        print(f"   Risk Score: {risk_score:.1%}")
        
        # Color code risk level
        if risk_level == "Critical":
            color = Fore.RED
            icon = "🚨"
            action = "BLOCK TRANSACTION - High fraud risk"
        elif risk_level == "Medium":
            color = Fore.YELLOW
            icon = "⚠️ "
            action = "REVIEW REQUIRED - Suspicious activity"
        else:
            color = Fore.GREEN
            icon = "✓"
            action = "ALLOW - Low risk detected"
        
        print(f"   Risk Level: {color}{icon} {risk_level}{Style.RESET_ALL}")
        print(f"   Recommended Action: {color}{action}{Style.RESET_ALL}")
        
        # Detailed warnings
        if fraud_prob > 0.5 or trans_flag == -1:
            print(f"\n{Fore.RED}⚠️  WARNING INDICATORS:{Style.RESET_ALL}")
            if fraud_prob > 0.7:
                print(f"   • High-confidence scam language detected")
            if trans_flag == -1:
                print(f"   • Unusual transaction pattern")
            if transaction[0] > 10000:
                print(f"   • Large transaction amount")
            if transaction[1] > 5:
                print(f"   • High urgency pressure")
            if transaction[2] == 1:
                print(f"   • New or unverified recipient")
        
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
    except Exception as e:
        print(f"{Fore.RED}Error during analysis: {str(e)}{Style.RESET_ALL}")

def quick_test_menu():
    """Show quick test options"""
    print(f"\n{Fore.CYAN}Quick Test Scenarios:{Style.RESET_ALL}")
    print("1. IRS Tax Scam")
    print("2. Tech Support Scam")
    print("3. Bank Security Scam")
    print("4. Legitimate Bank Call")
    print("5. Custom Scenario")
    print("0. Exit")
    
    choice = input("\nSelect option (0-5): ").strip()
    
    scenarios = {
        "1": {
            "transcript": "This is the IRS. You owe back taxes. Pay immediately via wire transfer or face arrest.",
            "transaction": [5000, 8, 1]
        },
        "2": {
            "transcript": "Microsoft support here. Your computer has a virus. Give us remote access and credit card now.",
            "transaction": [2500, 9, 1]
        },
        "3": {
            "transcript": "Bank fraud department. Verify your account number, PIN, and social security immediately.",
            "transaction": [10000, 7, 1]
        },
        "4": {
            "transcript": "Hello from your bank regarding your mortgage inquiry. Call us back at the number on your card.",
            "transaction": [500, 2, 0]
        }
    }
    
    if choice in scenarios:
        return scenarios[choice]["transcript"], scenarios[choice]["transaction"]
    elif choice == "5":
        return None, None
    else:
        return "exit", None

def main():
    """Main interactive loop"""
    print_header()
    
    while True:
        transcript, transaction = quick_test_menu()
        
        if transcript == "exit":
            print(f"\n{Fore.CYAN}Thank you for using TrustShield AI!{Style.RESET_ALL}\n")
            break
        
        if transcript is None:
            # Custom scenario
            transcript = get_transcript()
            if transcript.lower() in ['quit', 'exit']:
                print(f"\n{Fore.CYAN}Thank you for using TrustShield AI!{Style.RESET_ALL}\n")
                break
            transaction = get_transaction()
        
        analyze_scenario(transcript, transaction)
        
        continue_test = input(f"{Fore.CYAN}Test another scenario? (y/n): {Style.RESET_ALL}").strip().lower()
        if continue_test != 'y':
            print(f"\n{Fore.CYAN}Thank you for using TrustShield AI!{Style.RESET_ALL}\n")
            break

if __name__ == "__main__":
    main()
