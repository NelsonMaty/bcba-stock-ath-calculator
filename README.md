# BCBA Stock ATH Calculator

Calculates key metrics for BCBA (Buenos Aires Stock Exchange) stocks, including:

- Current price (CCL adjusted)
- All-Time High price (CCL adjusted)
- Upside potential to ATH
- Price to Book ratio

## Installation & Usage

1. Clone this repository to your local machine.
2. Run the following script to automatically set up the environment and run the program:

```bash
./run.sh
```
## Sort options

```bash
./run.sh --sort ticker  # Sort alphabetically by ticker
./run --sort upside  # Sort by upside potential to ATH
./run --sort pb      # Sort by Price/Book ratio
```

## Features

- CCL-adjusted price calculation using YPF stock for reference
- Historical ATH tracking since 2017
- Price to Book ratio from Yahoo Finance
- Configurable sorting options
- Coverage of both Panel Líder and Panel General stocks

## Data Source

Uses Yahoo Finance API via yfinance library for:

- Historical prices
- Book value data
- Real-time quotes

## Notes

- CCL calculation uses YPF's ratio between BCBA (YPFD) and NYSE (YPF) prices
- Some stocks might have missing P/B ratios if data is not available in Yahoo Finance
- Historical data starts from 2017-01-01
