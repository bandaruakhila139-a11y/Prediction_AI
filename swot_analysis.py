def generate_swot(
    team_expertise,
    innovation_level,
    market_competition,
    resource_availability,
    market_research
):
    strengths = []
    weaknesses = []
    opportunities = []
    threats = []

    # Strengths
    if team_expertise == "High":
        strengths.append("Strong technical team")
    if innovation_level == "High":
        strengths.append("High innovation potential")
    if resource_availability == "Good":
        strengths.append("Good resource availability")

    # Weaknesses
    if team_expertise == "Low":
        weaknesses.append("Limited technical expertise")
    if market_research == "Limited":
        weaknesses.append("Limited market research")
    if resource_availability == "Limited":
        weaknesses.append("Limited resources")

    # Opportunities
    if market_competition == "Low":
        opportunities.append("Low market competition")
    opportunities.append("Potential for market expansion")
    opportunities.append("Partnership opportunities")

    # Threats
    if market_competition == "High":
        threats.append("Strong competitors")
    threats.append("Rapid technology changes")
    threats.append("Market uncertainty")

    return {
        "Strengths": strengths,
        "Weaknesses": weaknesses,
        "Opportunities": opportunities,
        "Threats": threats
    }
