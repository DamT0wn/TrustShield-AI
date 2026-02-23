#!/usr/bin/env python3
"""
TrustShield AI - Automated Test Script
Tests all backend endpoints and AI models
"""

import requests
import sys
from colorama import init, Fore, Style

init(autoreset=True)

API_URL = "http://127.0.0.1:8000"

def print_test(name, status, message=""):
    """Print formatted test result"""
    if status == "PASS":
        print(f"{Fore.GREEN}✓ {name}{Style.RESET_ALL}")
    elif status == "FAIL":
        print(f"{Fore.RED}✗ {name}{Style.RESET_ALL}")
        if message:
            print(f"  {Fore.YELLOW}→ {message}{Style.RESET_ALL}")
    elif status == "SKIP":
        print(f"{Fore.YELLOW}⊘ {name} - {message}{Style.RESET_ALL}")

def test_backend_running():
    """Test if backend server is running"""
    try:
        response = requests.get(f"{API_URL}/docs", timeout=5)
        if response.status_code == 200:
            print_test("Backend Server Running", "PASS")
            return True
        else:
            print_test("Backend Server Running", "FAIL", f"Status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_test("Backend Server Running", "FAIL", "Cannot connect to server")
        return False
    except Exception as e:
        print_test("Backend Server Running", "FAIL", str(e))
        return False

def test_analyze_call():
    """Test /analyze-call endpoint"""
    try:
        response = requests.post(f"{API_URL}/analyze-call", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "transcript" in data and "fraud_probability" in data:
                print_test("Analyze Call Endpoint", "PASS")
                print(f"  Fraud Probability: {data['fraud_probability']:.2%}")
                return True
            else:
                print_test("Analyze Call Endpoint", "FAIL", "Missing expected fields")
                return False
        else:
            print_test("Analyze Call Endpoint", "FAIL", f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Analyze Call Endpoint", "FAIL", str(e))
        return False

def test_transaction_risk():
    """Test /transaction-risk endpoint"""
    try:
        response = requests.post(f"{API_URL}/transaction-risk", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "transaction_flag" in data:
                flag = data["transaction_flag"]
                status = "Anomaly" if flag == -1 else "Normal"
                print_test("Transaction Risk Endpoint", "PASS")
                print(f"  Transaction Status: {status}")
                return True
            else:
                print_test("Transaction Risk Endpoint", "FAIL", "Missing transaction_flag")
                return False
        else:
            print_test("Transaction Risk Endpoint", "FAIL", f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Transaction Risk Endpoint", "FAIL", str(e))
        return False

def test_final_risk():
    """Test /final-risk endpoint"""
    try:
        response = requests.post(f"{API_URL}/final-risk", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "risk_score" in data and "risk_level" in data:
                print_test("Final Risk Endpoint", "PASS")
                print(f"  Risk Score: {data['risk_score']:.2%}")
                print(f"  Risk Level: {data['risk_level']}")
                return True
            else:
                print_test("Final Risk Endpoint", "FAIL", "Missing expected fields")
                return False
        else:
            print_test("Final Risk Endpoint", "FAIL", f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Final Risk Endpoint", "FAIL", str(e))
        return False

def test_frontend():
    """Test if frontend is running"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print_test("Frontend Server Running", "PASS")
            return True
        else:
            print_test("Frontend Server Running", "FAIL", f"Status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_test("Frontend Server Running", "SKIP", "Not running (optional)")
        return None
    except Exception as e:
        print_test("Frontend Server Running", "FAIL", str(e))
        return False

def main():
    """Run all tests"""
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"TrustShield AI - Application Test Suite")
    print(f"{'='*50}{Style.RESET_ALL}\n")

    results = []

    # Test Backend
    print(f"{Fore.CYAN}Backend Tests:{Style.RESET_ALL}")
    results.append(test_backend_running())
    
    if results[-1]:  # Only test endpoints if backend is running
        results.append(test_analyze_call())
        results.append(test_transaction_risk())
        results.append(test_final_risk())
    else:
        print(f"\n{Fore.YELLOW}⚠ Backend not running. Start it with:{Style.RESET_ALL}")
        print(f"  cd trustshield-ai/backend")
        print(f"  uvicorn main:app --reload --host 127.0.0.1 --port 8000\n")
        results.extend([False, False, False])

    # Test Frontend
    print(f"\n{Fore.CYAN}Frontend Tests:{Style.RESET_ALL}")
    frontend_result = test_frontend()
    if frontend_result is None:
        print(f"\n{Fore.YELLOW}ℹ Frontend not running. Start it with:{Style.RESET_ALL}")
        print(f"  cd trustshield-ai/frontend")
        print(f"  npm start\n")
    else:
        results.append(frontend_result)

    # Summary
    passed = sum(1 for r in results if r is True)
    failed = sum(1 for r in results if r is False)
    total = len([r for r in results if r is not None])

    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"Test Summary")
    print(f"{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Passed: {passed}{Style.RESET_ALL}")
    print(f"{Fore.RED}Failed: {failed}{Style.RESET_ALL}")
    print(f"Total: {total}\n")

    if failed == 0 and passed > 0:
        print(f"{Fore.GREEN}✓ All tests passed! Application is working correctly.{Style.RESET_ALL}\n")
        sys.exit(0)
    elif passed == 0:
        print(f"{Fore.RED}✗ Application is not running. Please start the servers.{Style.RESET_ALL}\n")
        sys.exit(1)
    else:
        print(f"{Fore.YELLOW}⚠ Some tests failed. Check the errors above.{Style.RESET_ALL}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
