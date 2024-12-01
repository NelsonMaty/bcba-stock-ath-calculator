from tabulate import tabulate


def format_tables(df):
    df["upside"] = df.apply(
        lambda row: ((row["ath_usd"] / row["current_price_usd"]) - 1) * 100, axis=1
    )

    # Panel Líder table
    lider = df[df["panel"] == "Líder"].sort_values("upside", ascending=False)
    lider_table = lider[["ticker", "current_price_usd", "ath_usd", "upside"]].copy()
    lider_table.columns = ["Ticker", "Current USD", "ATH USD", "Upside %"]
    print("\n📈 Panel Líder")
    print(
        tabulate(
            lider_table,
            headers="keys",
            tablefmt="presto",
            floatfmt=(".0f", ".2f", ".2f", ".2f"),
            showindex=False,
        )
    )

    # Panel General table
    general = df[df["panel"] == "General"].sort_values("upside", ascending=False)
    general_table = general[["ticker", "current_price_usd", "ath_usd", "upside"]].copy()
    general_table.columns = ["Ticker", "Current USD", "ATH USD", "Upside %"]
    print("\n📊 Panel General")
    print(
        tabulate(
            general_table,
            headers="keys",
            tablefmt="presto",
            floatfmt=(".0f", ".2f", ".2f", ".2f"),
            showindex=False,
        )
    )

    # Sector leaders
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
