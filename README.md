# BCBA Stock ATH Calculator

Calculates key metrics for BCBA (Buenos Aires Stock Exchange) stocks, including:

- Current price (CCL adjusted)
- All-Time High price (CCL adjusted)
- Upside potential to ATH
- Price to Book ratio

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Basic usage (sorts by upside potential by default):

```bash
python main.py
```

Sort options:

```bash
python main.py --sort ticker  # Sort alphabetically by ticker
python main.py --sort upside  # Sort by upside potential to ATH
python main.py --sort pb      # Sort by Price/Book ratio
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
