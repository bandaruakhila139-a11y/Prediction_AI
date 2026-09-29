import pandas as pd

def get_market_data():
    data = {
        "year": [2020, 2021, 2022, 2023, 2024, 2025, 2026],
        "market_size": [120, 145, 175, 205, 245, 280, 320]
    }
    return pd.DataFrame(data)

def get_competitors():
    data = {
        "company": ["Competitor A", "Competitor B", "Competitor C"],
        "market_share": [28, 22, 15],
        "revenue": [45, 38, 25],
        "growth": [12, 8, 5]
    }
    return pd.DataFrame(data)

def get_market_summary():
    df = get_market_data()
    competitors = get_competitors()

    return {
        "tam": 2.4,
        "sam": 0.85,
        "som": 0.012,
        "market_growth": 8.2,
        "competitors": competitors.to_dict(orient="records"),
        "years": df["year"].tolist(),
        "market_values": df["market_size"].tolist()
    }
