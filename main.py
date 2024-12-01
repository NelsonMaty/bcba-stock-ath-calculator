import pandas as pd
import argparse
from config import STOCKS_DATA, START_DATE
from stock_utils import get_ccl_history, get_stock_data
from formatters import format_table


def parse_args():
    parser = argparse.ArgumentParser(description="BCBA Stock Analysis")
    parser.add_argument(
        "--sort",
        choices=["ticker", "upside", "pb"],
        default="upside",
        help="Sort criteria: ticker (alphabetical), upside (potential growth), pb (Price/Book ratio)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    results = []
    ccl = get_ccl_history(START_DATE)

    for ticker, info in STOCKS_DATA.items():
        stock_data = get_stock_data(ticker, ccl, START_DATE)
        if stock_data:
            stock_data["panel"] = info["panel"]
            results.append(stock_data)

    if results:
        df = pd.DataFrame(results)
        format_table(df, sort_by=args.sort)
    else:
        print("No results found")


if __name__ == "__main__":
    main()
