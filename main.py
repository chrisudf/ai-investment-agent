import os
from fastapi import FastAPI
from dotenv import load_dotenv
from agent.orchestrator import analyze_stock

# load_dotenv()

load_dotenv(dotenv_path=".env")  # 显式指定

print("API KEY:", os.getenv("OPENAI_API_KEY"))  # 调试用

app = FastAPI()

@app.get("/analyze")
async def analyze(ticker: str):
    result = await analyze_stock(ticker)
    return result