import yfinance as yf
import pandas as pd


tickers = ["^FCHI", "^GSPC",
    "AAPL", "MSFT", "GOOGL", "AMZN", "META",
    "TSLA", "NVDA", "JPM", "V", "JNJ",
    "PG", "XOM", "DIS", "HD", "BAC",
    "INTC", "PFE", "KO", "PEP", "CSCO"
]


# ------------------------------------------
# Download 10 years of data
# ------------------------------------------
data = yf.download(
    tickers,
    period="10y",
    interval="1d",
    auto_adjust=False
)

# Only keep closing prices
close_prices = data["Close"]

# ------------------------------------------
# Save to CSV
# ------------------------------------------
close_prices.to_csv("close_prices.csv")

print("Downloaded closing prices for:")
print(tickers)
print("Saved to 10yr_close_prices.csv")
