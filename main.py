import pandas as pd
from config import STOCKS_DATA, START_DATE
from stock_utils import get_ccl_history, get_stock_data
from formatters import format_tables


def main():
    results = []
    ccl = get_ccl_history(START_DATE)

    for ticker, info in STOCKS_DATA.items():
        stock_data = get_stock_data(ticker, ccl, START_DATE)
        if stock_data:
            stock_data["sector"] = info["sector"]
            stock_data["panel"] = info["panel"]
            results.append(stock_data)

    if results:
        df = pd.DataFrame(results)
        format_tables(df)
    else:
        print("No results found")


if __name__ == "__main__":
    main()
