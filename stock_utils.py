import yfinance as yf
import pandas as pd


def get_ccl_history(start_date):
    ypf_ar = yf.Ticker("YPFD.BA").history(start=start_date)["Close"]
    ypf_us = yf.Ticker("YPF").history(start=start_date)["Close"]

    # Normalize dates to date only, removing timezone info
    ypf_ar.index = ypf_ar.index.normalize().date
    ypf_us.index = ypf_us.index.normalize().date

    # Merge on date
    ccl = pd.DataFrame({"ar": ypf_ar, "us": ypf_us}).dropna()

    return ccl["ar"] / ccl["us"]


def get_stock_data(ticker, ccl, start_date):
    try:
        stock_info = yf.Ticker(f"{ticker}.BA")
        stock = stock_info.history(start=start_date)["Close"]
        stock.index = stock.index.normalize().date

        # Get book value ratio
        try:
            book_value = stock_info.info.get("bookValue", None)
            current_price = stock.iloc[-1]
            price_book_ratio = current_price / book_value if book_value else None
        except:
            price_book_ratio = None

        # Align dates with CCL
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
