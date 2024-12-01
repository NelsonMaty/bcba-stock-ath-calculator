from tabulate import tabulate


def format_tables(df):
    df["upside"] = df.apply(
        lambda row: ((row["ath_usd"] / row["current_price_usd"]) - 1) * 100, axis=1
    )
    results = df.sort_values("upside", ascending=False)

    main_table = results[["ticker", "current_price_usd", "ath_usd", "upside"]].copy()
    main_table.columns = ["Ticker", "Current USD", "ATH USD", "Upside %"]
    print("\n📈 Stocks by Upside Potential")
    print(
        tabulate(
            main_table,
            headers="keys",
            tablefmt="presto",
            floatfmt=(".0f", ".2f", ".2f", ".2f"),
            showindex=False,
        )
    )

    sector_max = df.loc[df.groupby("sector")["upside"].idxmax()]
    sector_max = sector_max.sort_values("upside", ascending=False)
    sector_table = sector_max[["sector", "ticker", "upside"]].copy()
    sector_table.columns = ["Sector", "Ticker", "Upside %"]
    print("\n🏆 Sector Leaders")
    print(
        tabulate(
            sector_table,
            headers="keys",
            tablefmt="presto",
            floatfmt=(".0f", ".0f", ".2f"),
            showindex=False,
        )
    )
