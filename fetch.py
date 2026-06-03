# fetch.py — ① 데이터 가져오기

import yfinance as yf
from datetime import datetime

# 관심 종목 목록: "이름": "티커코드"
TICKERS = {
    "코스피":   "^KS11",
    "원달러":   "KRW=X",
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
}

def fetch_data():
    """오늘 가격과 전일 대비 등락을 딕셔너리로 반환"""
    today = datetime.today().strftime("%Y-%m-%d")
    result = {}

    for name, ticker_code in TICKERS.items():
        ticker = yf.Ticker(ticker_code)
        hist = ticker.history(period="2d")  # 최근 2거래일 데이터

        if len(hist) < 1:
            continue  # 데이터 없으면 건너뜀

        today_price = hist["Close"].iloc[-1]
        yesterday_price = hist["Close"].iloc[-2] if len(hist) >= 2 else today_price
        change = today_price - yesterday_price
        change_pct = (change / yesterday_price) * 100 if yesterday_price else 0

        result[name] = {
            "date":       today,
            "ticker":     ticker_code,
            "price":      round(today_price, 2),
            "change":     round(change, 2),
            "change_pct": round(change_pct, 2),
        }

    return result


# 이 파일을 직접 실행할 때만 아래 코드가 동작
if __name__ == "__main__":
    data = fetch_data()
    for name, info in data.items():
        print(f"{name}: {info['price']} ({info['change_pct']:+.2f}%)")