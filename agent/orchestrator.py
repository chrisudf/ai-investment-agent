from agent.tools import get_stock_data
from llm.client import call_llm
import json
import re

# ✅ 开关：是否使用真实 LLM（避免消耗 token）
USE_LLM = True


async def analyze_stock(ticker: str):
    # ✅ 获取股票数据
    stock_data = get_stock_data(ticker)

    # ✅ 暂时不用 news（避免 429）
    news = [{"title": "No news available", "publisher": ""}]

    context = f"""
    Stock Data:
    {stock_data}

    News:
    {news}
    """

    # ✅ 如果关闭 LLM，直接返回 mock（不花钱）
    if not USE_LLM:
        return {
            "ticker": ticker,
            "analysis": {
                "company_overview": stock_data,
                "key_positives": ["Strong brand", "Stable revenue"],
                "key_risks": ["Market competition"],
                "summary": "Mock analysis (LLM disabled to save tokens)"
            }
        }

    # ✅ LLM prompt
    prompt = f"""
    You are a professional investment analyst.

    Analyze the following data for stock: {ticker}

    {context}

    Return JSON with:
    - company_overview
    - key_positives
    - key_risks
    - summary

    IMPORTANT:
    Return ONLY valid JSON.
    Do NOT wrap in markdown.
    Do NOT use ```json.
    """

    result = call_llm(prompt)

    # ✅ 清理 markdown
    cleaned = result.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    # ✅ 清理格式问题（防止 JSON 解析失败）
    cleaned = cleaned.replace("\n", " ")
    cleaned = re.sub(r",\s*}", "}", cleaned)
    cleaned = re.sub(r",\s*]", "]", cleaned)

    # ✅ 解析 JSON
    try:
        parsed = json.loads(cleaned)
    except Exception as e:
        print("JSON parse error:", e)
        print("RAW:", cleaned)
        parsed = {
            "error": "failed to parse",
            "raw": cleaned
        }

    return {
        "ticker": ticker,
        "analysis": parsed
    }
