def assess_five_risks(
    market_competition,
    team_expertise,
    resource_availability,
    innovation_level,
    market_research
):
    # Map the 5 specific risk categories to 1-5 scale
    
    # 1. Market Risk -> based on market_research
    market_risk = 4 if market_research == "Limited" else 3 if market_research == "Moderate" else 2
    
    # 2. Financial Risk -> based on resource_availability
    financial_risk = 4 if resource_availability == "Limited" else 3 if resource_availability == "Moderate" else 2
    
    # 3. Competition Risk -> based on market_competition
    competition_risk = 4 if market_competition == "High" else 3 if market_competition == "Medium" else 2
    
    # 4. Technical Risk -> based on innovation_level
    technical_risk = 4 if innovation_level == "Low" else 3 if innovation_level == "Medium" else 2
    
    # 5. Operational Risk -> based on team_expertise
    operational_risk = 4 if team_expertise == "Low" else 3 if team_expertise == "Medium" else 2
    
    return {
        "Market Risk": market_risk,
        "Financial Risk": financial_risk,
        "Competition Risk": competition_risk,
        "Technical Risk": technical_risk,
        "Operational Risk": operational_risk
    }

def calculate_risk(
    market_competition,
    team_expertise,
    resource_availability,
    innovation_level,
    market_research
):
    five_risks = assess_five_risks(market_competition, team_expertise, resource_availability, innovation_level, market_research)
    
    # Overall risk is the average of the 5 risks
    total_score = sum(five_risks.values()) / 5.0
    
    return {
        "score": total_score,
        "details": five_risks
    }


def get_risk_status(score):
    if score >= 4.0:
        return "HIGH RISK"
    elif score >= 3.0:
        return "MEDIUM RISK"
    else:
        return "LOW RISK"


def calculate_success_probability(risk_score):
    # Convert 1-5 scale back to a 0-100 probability (1 = 100%, 5 = 0%)
    prob = 100 - ((risk_score - 1) * 25)
    return max(0, min(100, prob))
