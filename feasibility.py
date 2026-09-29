def calculate_feasibility(risk_score, swot_data):
    """
    Calculates feasibility score based on overall risk and SWOT results.
    """
    # Base score
    score = 100
    
    # risk_score is 1-5. 
    # High risk (4-5) heavily impacts feasibility
    # risk penalty: score 5 -> -40 points, score 1 -> 0 points
    score -= ((risk_score - 1) * 10)
    
    # Add points for positive SWOT factors
    score += (len(swot_data.get("Strengths", [])) * 5)
    score += (len(swot_data.get("Opportunities", [])) * 5)
    
    # Subtract points for negative SWOT factors
    score -= (len(swot_data.get("Weaknesses", [])) * 5)
    score -= (len(swot_data.get("Threats", [])) * 5)
    
    # Clamp between 0 and 100
    score = max(0, min(100, score))
    
    return round(score)
