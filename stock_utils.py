import yfinance as yf
from yfinance import exceptions as yf_exceptions
import pandas as pd
import time
import random
from functools import wraps

REQUEST_INTERVAL = 0.6
JITTER = 0.3
MAX_RETRIES = 3

def rate_limited(fn):
    last_call = 0
    @wraps(fn)
    def wrapper(*args, **kwargs):
        nonlocal last_call
        retries = 0
        while retries <= MAX_RETRIES:
            elapsed = time.time() - last_call
            if elapsed < REQUEST_INTERVAL:
                sleep_time = REQUEST_INTERVAL - elapsed + random.uniform(0, JITTER)
                time.sleep(sleep_time)
            try:
                last_call = time.time()
                return fn(*args, **kwargs)
            except (yf_exceptions.YFRateLimitError, ConnectionError) as e:
                retries += 1
                if retries > MAX_RETRIES:
                    raise
                backoff = REQUEST_INTERVAL * (2 ** retries) + random.uniform(0, JITTER)
                time.sleep(backoff)
        return None
    return wrapper

@rate_limited
def safe_yfinance_request(ticker, field="history", **kwargs):
    obj = yf.Ticker(ticker)
    if field == "history":
        return obj.history(**kwargs)
    elif field == "info":
        return obj.info
    return obj


def get_ccl_history(start_date):
    ypf_ar = safe_yfinance_request("YPFD.BA", start=start_date)["Close"]
    ypf_us = safe_yfinance_request("YPF", start=start_date)["Close"]
    
    ypf_ar.index = ypf_ar.index.normalize().date
    ypf_us.index = ypf_us.index.normalize().date

    ccl = pd.DataFrame({"ar": ypf_ar, "us": ypf_us}).dropna()
    return ccl["ar"] / ccl["us"]


def get_stock_data(ticker, ccl, start_date):
    try:
        stock = safe_yfinance_request(f"{ticker}.BA", start=start_date)["Close"]
        stock.index = stock.index.normalize().date

        stock_info = safe_yfinance_request(f"{ticker}.BA", field="info")
        book_value = stock_info.get("bookValue", None)
        current_price = stock.iloc[-1]
        price_book_ratio = current_price / book_value if book_value else None

        data = pd.DataFrame({"price": stock, "ccl": ccl}).dropna()
        if data.empty:
            return None

        adjusted_prices = data["price"] / data["ccl"]

        return {
            "ticker": ticker,
            "first_available_date": data.index[0].strftime("%Y-%m-%d"),
            "current_price_usd": round(float(adjusted_prices.iloc[-1]), 2),
            "ath_usd": round(float(adjusted_prices.max()), 2),
            "ath_date": adjusted_prices.idxmax().strftime("%Y-%m-%d"),
            "pct_from_ath": round(
                float(
                    (adjusted_prices.iloc[-1] - adjusted_prices.max())
                    / adjusted_prices.max()
                    * 100
                ),
                2,
            ),
            "p/b": round(float(price_book_ratio), 2) if price_book_ratio else None,
        }
    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        return None
