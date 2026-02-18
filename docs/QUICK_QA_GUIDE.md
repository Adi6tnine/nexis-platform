# NEXIS - Quick Q&A Guide for Judges/Regulators

## Basic Understanding

### Q1: What is NEXIS in simple terms?
**A:** NEXIS is like CIBIL, but for people who don't have a CIBIL score. It uses UPI transactions, utility bill payments, and banking behavior to create a credit score (300-900 range).

### Q2: Who is it for?
**A:** India's 190 million "credit-invisible" people:
- Gig workers (Uber drivers, delivery partners)
- Small shop owners
- Rural population
- Young professionals with no credit history
- Anyone without a CIBIL score

### Q3: How is it different from CIBIL?
**A:** 
- **CIBIL**: Uses credit card, loan history
- **NEXIS**: Uses UPI, utility bills, bank account behavior
- **CIBIL**: Only for people with credit history
- **NEXIS**: For people WITHOUT credit history

---

## Scoring Process

### Q4: How is the score calculated?
**A:** 4-step process:
1. **Collect data**: UPI transactions, utility bills, bank account
2. **Engineer features**: Convert to 20 numerical features
3. **ML model**: Random Forest predicts risk (Low/Moderate/High)
4. **Convert to score**: Risk + confidence → Score (300-900)

### Q5: What data is used?
**A:** Financial behavior only:
- ✓ UPI transaction patterns
- ✓ Utility bill payment history
- ✓ Bank account balance trends
- ✓ Savings growth
- ✓ Income regularity
- ✓ Address stability

### Q6: What data is NOT used?
**A:** No discriminatory data:
- ❌ Caste
- ❌ Religion
- ❌ Gender
- ❌ Location/PIN code
- ❌ Political views
- ❌ Social media

### Q7: Can users see why they got their score?
**A:** Yes! Every score includes:
- Exact score (e.g., 785)
- Risk level (Low/Moderate/High)
- Top 3-5 factors that influenced the score
- Clear explanations in simple language

**Example:**
```
✓ Excellent Payment History (High Impact)
  "You've paid utility bills on time for 18 months"

✓ Established Account (High Impact)
  "Your bank account is 3.5 years old"
```

---

## Lender Portal

### Q8: What is the Lender Portal?
**A:** A dashboard for banks/NBFCs to review loan applications. Shows:
- Applicant's trust score
- AI recommendation (approve/decline/request data)
- Behavioral metrics
- Decision panel for human lender

### Q9: Does AI make the lending decision?
**A:** **NO!** 
- AI only provides **recommendation**
- **Human lender** makes final decision
- Lender must provide written justification
- This is called "Human-in-the-Loop"

### Q10: Why not let AI decide?
**A:** Multiple reasons:
1. **Accountability**: Humans are responsible, not machines
2. **Fairness**: Humans can override AI biases
3. **Compliance**: RBI requires human oversight
4. **Flexibility**: Special cases need human judgment
5. **Trust**: People trust human decisions more

### Q11: What are the lender's options?
**A:** Three choices:
1. **Approve with Terms**: Set loan amount, interest rate, term
2. **Request More Data**: Ask for additional documents
3. **Decline**: Reject the application

All require written justification (minimum 20 characters).

### Q12: What if lender disagrees with AI?
**A:** Lender can override AI recommendation with justification.

**Example:**
- AI says: "Approve"
- Lender decides: "Decline"
- Reason: "Applicant's income is seasonal (farming), need 2 years data"
- This is recorded in audit trail

---

## Fairness & Compliance

### Q13: How is discrimination prevented?
**A:** Multiple safeguards:
1. No caste/religion/gender data collected
2. No location-based scoring
3. Only financial behavior analyzed
4. Human oversight on all decisions
5. Audit trail for regulatory review

### Q14: What if the AI is biased?
**A:** 
1. Human lender can override AI
2. All decisions are audited
3. Patterns of bias can be detected
4. Model can be retrained
5. Regulatory oversight enabled

### Q15: Is user data safe?
**A:** Yes, multiple protections:
- Passwords encrypted (bcrypt)
- Data transmission encrypted (HTTPS)
- Consent required before use
- User can delete data anytime
- Complies with Data Protection Act 2023

### Q16: What laws does it comply with?
**A:** 
- Reserve Bank of India (RBI) guidelines
- Digital Personal Data Protection Act, 2023
- KYC/AML regulations
- Fair Practices Code for Lenders
- Indian Constitution (no discrimination)

---

## Technical Details

### Q17: What ML algorithm is used?
**A:** Random Forest Classifier
- 100 decision trees
- Each tree votes on risk category
- Majority vote wins
- 92% accuracy on test data

### Q18: How is explainability achieved?
**A:** SHAP (SHapley Additive exPlanations)
- Calculates each feature's contribution
- Shows which factors increased/decreased score
- Translates to human-readable explanations
- No "black box" decisions

### Q19: How accurate is the model?
**A:** 
- Training accuracy: 95%
- Test accuracy: 92%
- Confidence scores provided (e.g., 85%)
- Continuously monitored and improved

### Q20: Can the model be audited?
**A:** Yes, completely:
- All predictions logged
- Feature values stored
- SHAP values recorded
- Decision trail maintained
- Available for regulatory review

---

## Audit & Accountability

### Q21: What is recorded in the audit trail?
**A:** Everything:
- User ID
- Trust score
- AI recommendation
- AI confidence
- Human decision
- Written justification
- Loan terms (if approved)
- Lender ID
- Timestamp
- Decision officer name

### Q22: Who can access audit trails?
**A:** 
- Regulators (RBI, etc.)
- Internal compliance team
- External auditors
- Courts (with proper authorization)

### Q23: How long is data retained?
**A:** 
- Active users: As long as account exists
- Audit trails: 7 years (regulatory requirement)
- Deleted accounts: 90 days (backup retention)

---

## Real-World Scenarios

### Q24: Example - Uber Driver
**Scenario:** Rajesh drives Uber, needs ₹50,000 for vehicle repair

**NEXIS Analysis:**
- UPI earnings: ₹40,000/month consistently
- Fuel payments: Regular, predictable
- Utility bills: Paid on time for 18 months
- Savings: Growing by 10% yearly

**Result:**
- Trust Score: 785
- Risk: Low
- AI Recommendation: Approve
- Lender Decision: Approved at 15% p.a. for 12 months

### Q25: Example - Kirana Store Owner
**Scenario:** Priya owns small shop, needs ₹2,00,000 for inventory

**NEXIS Analysis:**
- UPI QR code: 200+ transactions/month
- Supplier payments: Regular via UPI
- Electricity bill: Always on time
- GST filing: Regular (optional data)

**Result:**
- Trust Score: 742
- Risk: Low-Moderate
- AI Recommendation: Approve with guidance
- Lender Decision: Approved at 18% p.a. for 6 months

### Q26: Example - Declined Application
**Scenario:** Amit, recent graduate, needs ₹1,00,000

**NEXIS Analysis:**
- Bank account: Only 3 months old
- Income: Irregular (freelance)
- Utility bills: Only 2 months history
- Savings: Minimal

**Result:**
- Trust Score: 520
- Risk: Moderate-High
- AI Recommendation: Request more data
- Lender Decision: Declined
- Reason: "Insufficient financial history. Recommend reapplication after 6 months of stable income."

---

## Common Concerns

### Q27: Can rich people game the system?
**A:** Difficult because:
- Not just about balance, but behavior patterns
- Consistency matters more than amount
- Volatility is penalized
- Long-term patterns analyzed
- Human lender reviews all decisions

### Q28: What about privacy concerns?
**A:** Strong protections:
- Explicit consent required
- User can withdraw consent anytime
- Data minimization (only necessary data)
- Encrypted storage and transmission
- No data sharing without permission
- Complies with Data Protection Act 2023

### Q29: Can lenders misuse the system?
**A:** Prevented by:
- All decisions recorded
- Written justifications required
- Audit trails maintained
- Regulatory oversight
- Pattern analysis for discrimination
- Lender accountability

### Q30: What if user disputes their score?
**A:** User can:
1. View detailed explanation
2. Request data review
3. Provide additional information
4. Request re-scoring
5. File complaint with grievance officer
6. Approach regulator if unresolved

---

## Future Enhancements

### Q31: What's next for NEXIS?
**A:** Planned improvements:
- Hindi and regional language support
- Mobile app (Android/iOS)
- Aadhaar integration
- Account Aggregator API
- WhatsApp bot for score check
- Voice-based interface
- Rural outreach program

### Q32: Will it replace CIBIL?
**A:** No, it complements CIBIL:
- CIBIL: For people with credit history
- NEXIS: For people without credit history
- Both can coexist
- Eventually may integrate with CIBIL

---

## Key Takeaways

1. **Purpose**: Enable lending to credit-invisible Indians
2. **Method**: ML-based scoring using alternative data
3. **Fairness**: No discrimination, human oversight
4. **Transparency**: Explainable scores, audit trails
5. **Compliance**: RBI guidelines, data protection laws
6. **Accountability**: Humans decide, AI only advises

---

## Contact Information

**For Technical Questions:**
- Email: tech@nexis.in

**For Compliance Questions:**
- Email: compliance@nexis.in

**For Regulatory Inquiries:**
- Email: regulatory@nexis.in
- Phone: +91 XXXXX XXXXX

**Grievance Officer:**
- Email: grievance@nexis.in

---

**Document Version:** 1.0  
**Last Updated:** February 17, 2026  
**For:** Judicial/Regulatory Review
