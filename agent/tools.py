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
    try:
        url = f"https://query1.finance.yahoo.com/v1/finance/search?q={ticker}"
        res = requests.get(url, timeout=5)

        # ✅ 打印调试（关键）
        print("STATUS:", res.status_code)
        print("TEXT:", res.text[:200])

        # ✅ 如果不是 200，直接返回
        if res.status_code != 200:
            return [{"error": f"status {res.status_code}"}]

        # ✅ 尝试解析 JSON
        try:
            data = res.json()
        except Exception:
            return [{"error": "not json response"}]

        news = data.get("news", [])[:5]

        if not news:
            return [{"info": "no news found"}]

        return [
            {
                "title": n.get("title", ""),
                "publisher": n.get("publisher", "")
            }
            for n in news
        ]

    except Exception as e:
        return [{"error": str(e)}]