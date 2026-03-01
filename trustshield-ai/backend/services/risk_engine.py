"""
Enhanced Risk Engine with multi-factor risk assessment.
"""

def calculate_risk(voice_prob, transaction_flag, confidence=0.85):
    """
    Calculate final risk score using weighted multi-factor analysis.
    
    Args:
        voice_prob: Fraud probability from voice analysis (0-1)
        transaction_flag: Anomaly flag from transaction analysis (-1 or 1)
        confidence: Confidence level of voice analysis (0-1)
    
    Returns:
        (final_score, risk_level)
    """
    # Transaction risk score
    transaction_score = 1.0 if transaction_flag == -1 else 0.0
    
    # Apply confidence weighting to voice probability
    weighted_voice = voice_prob * confidence
    
    # Weighted combination (voice is primary indicator)
    final_score = (weighted_voice * 0.65) + (transaction_score * 0.35)
    
    # Risk level classification with refined thresholds
    if final_score >= 0.75:
        level = "Critical"
    elif final_score >= 0.50:
        level = "Medium"
    elif final_score >= 0.25:
        level = "Low"
    else:
        level = "Minimal"
    
    return final_score, level

def calculate_detailed_risk(voice_analysis, transaction_analysis, behavioral_factors=None):
    """
    Advanced risk calculation with multiple data sources.
    
    Args:
        voice_analysis: Dict with fraud_probability, confidence, risk_factors
        transaction_analysis: Dict with anomaly_flag, risk_indicators
        behavioral_factors: Optional dict with additional behavioral signals
    
    Returns:
        Dict with detailed risk assessment
    """
    voice_prob = voice_analysis.get("fraud_probability", 0)
    voice_confidence = voice_analysis.get("confidence", 0.85)
    transaction_flag = transaction_analysis.get("anomaly_flag", 1)
    
    # Base risk calculation
    base_score, base_level = calculate_risk(voice_prob, transaction_flag, voice_confidence)
    
    # Apply behavioral adjustments if available
    behavioral_adjustment = 0
    if behavioral_factors:
        if behavioral_factors.get("repeat_caller", False):
            behavioral_adjustment += 0.1
        if behavioral_factors.get("known_scammer_pattern", False):
            behavioral_adjustment += 0.15
        if behavioral_factors.get("verified_customer", False):
            behavioral_adjustment -= 0.2
    
    # Final adjusted score
    adjusted_score = min(1.0, max(0.0, base_score + behavioral_adjustment))
    
    # Recalculate level with adjusted score
    if adjusted_score >= 0.75:
        final_level = "Critical"
    elif adjusted_score >= 0.50:
        final_level = "Medium"
    elif adjusted_score >= 0.25:
        final_level = "Low"
    else:
        final_level = "Minimal"
    
    return {
        "risk_score": adjusted_score,
        "risk_level": final_level,
        "base_score": base_score,
        "behavioral_adjustment": behavioral_adjustment,
        "confidence": voice_confidence
    }