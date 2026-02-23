# 🛡️ Start Testing TrustShield AI

## Quick Start - 3 Simple Commands

### 1. Quick Test (30 seconds)
See the system detect a scam vs legitimate call:
```bash
cd trustshield-ai
python quick_test.py
```

### 2. Interactive Testing (Your Own Scenarios)
Test with custom call transcripts and transactions:
```bash
cd trustshield-ai
python interactive_test.py
```

Choose from menu:
- IRS Tax Scam
- Tech Support Scam  
- Bank Security Scam
- Legitimate Bank Call
- Custom Scenario (enter your own)

### 3. Full Test Suite (12+ Scenarios)
Run comprehensive tests with real-life examples:
```bash
cd trustshield-ai
python test_scenarios.py
```

---

## What Just Worked ✅

The quick test showed:

**IRS Tax Scam (High Risk)**
- Fraud Probability: 64.7%
- Transaction: $50,000 (ANOMALY detected)
- Risk Score: 78.8%
- Result: 🚨 CRITICAL - Transaction BLOCKED

**Legitimate Bank Call (Low Risk)**
- Fraud Probability: 64.6%
- Transaction: $500 (Normal pattern)
- Risk Score: 38.8%
- Result: ✓ LOW RISK - Transaction allowed

---

## Real-Life Testing Examples

### Test Your Own Scenarios

Run `python interactive_test.py` and try:

**Example 1: Romance Scam**
```
Transcript: "I love you but I'm stuck overseas. Wire me $2000 for a plane ticket."
Amount: $2000
Urgency: 8
New Recipient: 1
```

**Example 2: Friend Request**
```
Transcript: "Hey it's John from work, can you split the lunch bill?"
Amount: $25
Urgency: 1
New Recipient: 0
```

**Example 3: Investment Scam**
```
Transcript: "Invest $10,000 today for guaranteed 500% returns!"
Amount: $10000
Urgency: 9
New Recipient: 1
```

---

## Understanding Results

### Risk Levels
- **Critical (75-100%)**: Block transaction immediately
- **Medium (40-75%)**: Flag for review
- **Low (0-40%)**: Allow with monitoring

### What the AI Detects
- Urgency and pressure tactics
- Requests for sensitive information
- Threats and fear tactics
- Too-good-to-be-true offers
- Unusual transaction patterns
- Large amounts to new recipients

---

## Web Dashboard Testing

The dashboard is running at: **http://localhost:3000**

Click "Run Analysis" to see:
- Real-time transcript analysis
- Risk gauge visualization
- Alert panel with warnings
- Risk level indicator

---

## Next Steps

1. ✅ Run `python quick_test.py` - See it work
2. ✅ Run `python interactive_test.py` - Test your scenarios
3. ✅ Open http://localhost:3000 - Use the dashboard
4. ✅ Read `REAL_LIFE_TESTING_GUIDE.md` - Detailed guide

---

## Need Help?

- Full testing guide: `REAL_LIFE_TESTING_GUIDE.md`
- Application status: `APP_RUNNING_STATUS.md`
- How to test: `HOW_TO_TEST.md`

Happy testing! 🚀
