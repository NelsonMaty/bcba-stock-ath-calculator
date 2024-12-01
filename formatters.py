from tabulate import tabulate


def format_table(df, sort_by="upside"):
    # Calculate upside if not already present
    if "upside" not in df.columns:
        df["upside"] = df.apply(
            lambda row: ((row["ath_usd"] / row["current_price_usd"]) - 1) * 100, axis=1
        )

    # Sort based on argument
    sort_column = {"ticker": "ticker", "upside": "upside", "pb": "p/b"}.get(sort_by)

    # Define ascending based on sort type
    ascending = {
        "ticker": True,
        "upside": False,
        "pb": True,  # Changed to True to show lowest P/B first
    }.get(sort_by)

    df_sorted = df.sort_values(sort_column, ascending=ascending)

    # Prepare table data
    table_data = df_sorted[
        ["ticker", "panel", "current_price_usd", "ath_usd", "upside", "p/b"]
    ].copy()
    table_data.columns = [
        "Ticker",
        "Panel",
        "Current USD",
        "ATH USD",
        "Upside %",
        "P/B",
    ]

    print(f"\n📈 BCBA Stocks Analysis (sorted by {sort_by})")
    print(
        tabulate(
            table_data,
            headers="keys",
            tablefmt="presto",
            floatfmt=(".0f", ".0f", ".2f", ".2f", ".2f", ".2f"),
            showindex=False,
        )
    )
