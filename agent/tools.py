import yfinance as yf
import requests

def get_stock_data(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "name": info.get("longName"),
        "sector": info.get("sector"),
        "marketCap": info.get("marketCap"),
        "price": info.get("currentPrice")
    }

def get_company_news(ticker: str):
    url = f"https://query1.finance.yahoo.com/v1/finance/search?q={ticker}"
    res = requests.get(url).json()

    news = res.get("news", [])[:5]

    return [
        {
            "title": n.get("title"),
            "publisher": n.get("publisher")
        }
        for n in news
    ]