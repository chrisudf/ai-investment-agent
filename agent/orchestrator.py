from agent.tools import get_stock_data, get_company_news
from llm.client import call_llm

async def analyze_stock(ticker: str):
    stock_data = get_stock_data(ticker)
    news = get_company_news(ticker)

    context = f"""
    Stock Data:
    {stock_data}

    News:
    {news}
    """

    prompt = f"""
    You are a professional investment analyst.

    Analyze the following data for stock: {ticker}

    {context}

    Return JSON with:
    - company_overview
    - key_positives
    - key_risks
    - summary
    """

    result = call_llm(prompt)

    return {
        "ticker": ticker,
        "analysis": result
    }