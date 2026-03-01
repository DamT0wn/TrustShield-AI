"""
TrustShield AI - Complete Demo Pipeline Test
Tests the full call analysis pipeline end-to-end
"""
import requests
import json
from colorama import Fore, Style, init

init(autoreset=True)

API_URL = "http://127.0.0.1:8000"

def print_header(text):
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}{text.center(70)}")
    print(f"{Fore.CYAN}{'='*70}\n")

def print_success(text):
    print(f"{Fore.GREEN}✓ {text}")

def print_error(text):
    print(f"{Fore.RED}✗ {text}")

def print_info(text):
    print(f"{Fore.YELLOW}ℹ {text}")

def test_api_health():
    """Test if API is running."""
    print_header("Testing API Health")
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"API is online: {data.get('service')}")
            print_info(f"Version: {data.get('version')}")
            print_info(f"Available endpoints: {', '.join(data.get('endpoints', []))}")
            return True
        else:
            print_error(f"API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to API. Is the backend running?")
        print_info("Start backend: cd trustshield-ai/backend && python -m uvicorn main:app --reload")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_demo_scenarios():
    """Test available demo scenarios."""
    print_header("Testing Demo Scenarios")
    try:
        response = requests.get(f"{API_URL}/demo-scenarios", timeout=5)
        if response.status_code == 200:
            data = response.json()
            scenarios = data.get('scenarios', [])
            print_success(f"Found {len(scenarios)} demo scenarios")
            for scenario in scenarios:
                details = data['details'].get(scenario, {})
                print_info(f"  - {scenario}: Risk={details.get('expected_risk')}")
            return True
        else:
            print_error(f"Failed to get scenarios: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_full_analysis(scenario_name):
    """Test full analysis pipeline with a specific scenario."""
    print_header(f"Testing Full Analysis: {scenario_name}")
    try:
        payload = {"demo_scenario": scenario_name}
        response = requests.post(f"{API_URL}/full-analysis", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Display transcript
            print(f"{Fore.CYAN}Transcript:")
            transcript = data.get('transcript', '')
            print(f"{Fore.WHITE}{transcript[:200]}..." if len(transcript) > 200 else transcript)
            
            # Voice analysis
            voice = data.get('voice_analysis', {})
            print(f"\n{Fore.CYAN}Voice Analysis:")
            print_info(f"Fraud Probability: {voice.get('fraud_probability', 0):.2%}")
            print_info(f"Confidence: {voice.get('confidence', 0):.2%}")
            
            risk_factors = voice.get('risk_factors', [])
            if risk_factors:
                print(f"{Fore.YELLOW}Risk Factors:")
                for factor in risk_factors:
                    print(f"  • {factor}")
            
            # Transaction analysis
            transaction = data.get('transaction_analysis', {})
            print(f"\n{Fore.CYAN}Transaction Analysis:")
            print_info(f"Anomalous: {transaction.get('is_anomalous', False)}")
            
            indicators = transaction.get('risk_indicators', [])
            if indicators:
                print(f"{Fore.YELLOW}Risk Indicators:")
                for indicator in indicators:
                    print(f"  • {indicator}")
            
            # Final risk
            final = data.get('final_risk', {})
            risk_score = final.get('risk_score', 0)
            risk_level = final.get('risk_level', 'Unknown')
            
            print(f"\n{Fore.CYAN}Final Risk Assessment:")
            
            # Color code based on risk level
            if risk_level == "Critical":
                color = Fore.RED
            elif risk_level == "Medium":
                color = Fore.YELLOW
            else:
                color = Fore.GREEN
            
            print(f"{color}Risk Score: {risk_score:.2%}")
            print(f"{color}Risk Level: {risk_level}")
            print_info(f"Recommendation: {final.get('recommendation', 'N/A')}")
            
            # Alerts
            alerts = final.get('alerts', [])
            if alerts:
                print(f"\n{Fore.CYAN}Alerts:")
                for alert in alerts:
                    print(f"  {alert}")
            
            print_success(f"Full analysis completed successfully for {scenario_name}")
            return True
        else:
            print_error(f"Analysis failed: {response.status_code}")
            print_error(response.text)
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_all_scenarios():
    """Test all available demo scenarios."""
    scenarios = [
        "bank_scam",
        "irs_scam", 
        "tech_support_scam",
        "grandparent_scam",
        "legitimate_call",
        "legitimate_business"
    ]
    
    results = []
    for scenario in scenarios:
        result = test_full_analysis(scenario)
        results.append((scenario, result))
        print()  # Spacing between tests
    
    # Summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for scenario, result in results:
        if result:
            print_success(f"{scenario}: PASSED")
        else:
            print_error(f"{scenario}: FAILED")
    
    print(f"\n{Fore.CYAN}Total: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("All tests passed! System is ready for demo.")
    else:
        print_error(f"{total - passed} test(s) failed. Please review errors above.")

def main():
    print(f"{Fore.MAGENTA}{Style.BRIGHT}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║           TrustShield AI - Demo Pipeline Test Suite              ║")
    print("║                  Complete End-to-End Testing                      ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(Style.RESET_ALL)
    
    # Test API health first
    if not test_api_health():
        print_error("\nCannot proceed without backend API. Please start the backend first.")
        return
    
    print()
    
    # Test demo scenarios endpoint
    if not test_demo_scenarios():
        print_error("\nDemo scenarios endpoint failed. Continuing with manual tests...")
    
    print()
    
    # Test all scenarios
    test_all_scenarios()
    
    print_header("Testing Complete")
    print_info("Frontend URL: http://localhost:3000")
    print_info("Backend API: http://127.0.0.1:8000")
    print_info("API Docs: http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    main()
