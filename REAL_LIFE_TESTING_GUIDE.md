# TrustShield AI - Real-Life Testing Guide

## Testing Options

You have 3 ways to test the application with real-life scenarios:

### 1. Interactive Testing Tool (Recommended for Custom Tests)
Test with your own custom scenarios in real-time.

```bash
cd trustshield-ai
python interactive_test.py
```

**Features:**
- Quick test menu with pre-built scam scenarios
- Custom scenario input
- Real-time fraud analysis
- Detailed risk assessment with recommendations
- Color-coded results

**Use Cases:**
- Test specific call transcripts you encounter
- Experiment with different transaction amounts
- See how urgency affects risk scores
- Compare legitimate vs scam patterns

---

### 2. Automated Scenario Testing
Run comprehensive tests with 12+ real-life scenarios.

```bash
cd trustshield-ai
python test_scenarios.py
```

**Includes:**
- 5 High-risk scam scenarios (IRS, tech support, grandparent scams)
- 3 Medium-risk suspicious calls
- 4 Low-risk legitimate calls
- Automatic pass/fail validation
- Detailed summary report

**Use Cases:**
- Validate the AI models are working correctly
- Benchmark detection accuracy
- Demonstrate the system to stakeholders
- Regression testing after changes

---

### 3. Web Dashboard Testing
Use the browser interface for visual testing.

1. Open: http://localhost:3000
2. Click "Run Analysis" button
3. See real-time results with:
   - Transcript display
   - Risk gauge visualization
   - Alert panel
   - Risk level indicator

**Use Cases:**
- Demo to non-technical users
- Visual presentation
- End-user experience testing
- Integration testing

---

## Real-Life Test Scenarios Included

### High-Risk Scams (Should Detect as Critical)

1. **IRS Tax Scam**
   - Threatens arrest for unpaid taxes
   - Demands immediate wire transfer
   - Uses fear and urgency tactics

2. **Tech Support Scam**
   - Claims to be Microsoft/Apple support
   - Requests remote access
   - Demands credit card for "virus removal"

3. **Grandparent Scam**
   - Pretends to be family member in trouble
   - Requests bail money urgently
   - Asks to keep it secret

4. **Bank Security Scam**
   - Claims to be fraud department
   - Requests account numbers and PIN
   - Creates false sense of urgency

5. **Lottery/Prize Scam**
   - Claims you won money
   - Requires upfront payment for "fees"
   - Too good to be true offer

### Medium-Risk Scenarios

1. **Suspicious Charity Call**
   - Requests immediate credit card info
   - High-pressure tactics
   - Unverified organization

2. **Pressure Sales Call**
   - Limited time offer
   - Must decide immediately
   - Aggressive tactics

3. **Vague Emergency**
   - Unclear about the issue
   - Demands callback to unknown number
   - Creates unnecessary urgency

### Low-Risk Legitimate Calls

1. **Legitimate Bank Call**
   - Provides verification method
   - No pressure tactics
   - Professional communication

2. **Appointment Reminder**
   - Simple reminder
   - No financial requests
   - Expected communication

3. **Customer Service Follow-up**
   - Post-purchase check-in
   - No requests for information
   - Helpful tone

4. **Known Contact**
   - Personal communication
   - No financial transaction
   - Normal conversation

---

## How to Test Your Own Scenarios

### Using Interactive Tool:

1. Run: `python interactive_test.py`
2. Choose option 5 (Custom Scenario)
3. Enter the call transcript
4. Enter transaction details:
   - Amount: Dollar amount being transferred
   - Urgency: 0-10 scale (0=no rush, 10=extreme pressure)
   - New Recipient: 0=known contact, 1=new/unknown

### Example Custom Tests:

**Test 1: Romance Scam**
```
Transcript: "I love you but I'm stuck overseas and need money for a plane ticket. 
Please wire $2000 to this account so we can finally meet."

Amount: $2000
Urgency: 7
New Recipient: 1
```

**Test 2: Legitimate Friend Request**
```
Transcript: "Hey, it's John from work. Can you split the lunch bill from yesterday? 
I'll Venmo you back tomorrow."

Amount: $25
Urgency: 1
New Recipient: 0
```

**Test 3: Investment Scam**
```
Transcript: "This is a once-in-a-lifetime investment opportunity. You must invest 
$10,000 today or miss out on guaranteed returns of 500%."

Amount: $10000
Urgency: 9
New Recipient: 1
```

---

## Understanding the Results

### Fraud Probability
- **0-40%**: Low risk - Likely legitimate
- **40-70%**: Medium risk - Suspicious, needs review
- **70-100%**: High risk - Strong scam indicators

### Transaction Anomaly
- **Normal (1)**: Transaction pattern is typical
- **Anomaly (-1)**: Unusual pattern detected

### Risk Levels
- **Low**: Allow transaction, minimal monitoring
- **Medium**: Flag for review, additional verification needed
- **Critical**: Block transaction, high fraud probability

### Warning Indicators
The system checks for:
- Scam language patterns (urgency, threats, requests for info)
- Large transaction amounts (>$10,000)
- High urgency pressure (>5/10)
- New or unverified recipients
- Unusual transaction patterns

---

## Testing Best Practices

1. **Test Edge Cases**
   - Very small amounts ($1-10)
   - Very large amounts ($100,000+)
   - Zero urgency vs maximum urgency
   - Known vs unknown recipients

2. **Test Language Variations**
   - Different scam scripts
   - Broken English (common in scams)
   - Professional vs casual language
   - Emotional manipulation tactics

3. **Test Transaction Patterns**
   - Single large transaction
   - Multiple small transactions
   - Transactions to new recipients
   - Transactions with high urgency

4. **Compare Results**
   - Run same transcript with different transaction amounts
   - Run different transcripts with same transaction
   - Test legitimate calls with suspicious transactions

5. **Document Findings**
   - Note false positives (legitimate flagged as scam)
   - Note false negatives (scam not detected)
   - Track accuracy across different scam types

---

## Expected Performance

### Detection Accuracy Goals
- High-risk scams: >90% detection rate
- Medium-risk: >70% detection rate
- Legitimate calls: <10% false positive rate

### Response Times
- Analysis: <2 seconds
- Risk calculation: <1 second
- Total processing: <3 seconds

---

## Troubleshooting

### Issue: Low fraud scores for obvious scams
**Solution:** The model needs more training data. Add examples to `datasets/scam_texts.csv`

### Issue: High false positives
**Solution:** Adjust risk thresholds in `backend/services/risk_engine.py`

### Issue: Transaction anomaly not detecting
**Solution:** The Isolation Forest model needs more training data with varied patterns

---

## Next Steps After Testing

1. **Collect Real Data**
   - Record actual scam calls (with permission)
   - Gather legitimate call examples
   - Build larger training dataset

2. **Fine-tune Models**
   - Adjust risk thresholds based on test results
   - Retrain with more diverse examples
   - Add more scam patterns

3. **Add Features**
   - Voice analysis (tone, stress detection)
   - Caller ID verification
   - Historical pattern matching
   - Real-time alerts

4. **Deploy**
   - Set up production environment
   - Configure monitoring and logging
   - Implement user feedback loop
   - Create incident response procedures

---

## Quick Start Commands

```bash
# Interactive testing (custom scenarios)
cd trustshield-ai
python interactive_test.py

# Automated testing (pre-built scenarios)
cd trustshield-ai
python test_scenarios.py

# Web dashboard
# Already running at http://localhost:3000
```

Happy testing! 🛡️
