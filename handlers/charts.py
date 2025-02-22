import requests
import matplotlib.pyplot as plt
import datetime
import os
from telegram import Update
from telegram.ext import CallbackContext

# Alpha Vantage API URL
BASE_URL = "https://www.alphavantage.co/query"

def get_stock_history(symbol: str, api_key: str, days: int = 30):
    """Fetch historical stock data for the last `days` days."""
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol.upper(),
        "apikey": api_key
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "Time Series (Daily)" in data:
        time_series = data["Time Series (Daily)"]
        dates = sorted(time_series.keys(), reverse=True)[:days]  # Get last `days` dates

        history = {
            "dates": dates[::-1],
            "prices": [float(time_series[date]["4. close"]) for date in dates[::-1]]
        }
        return history
    else:
        return None

def generate_stock_chart(symbol: str, stock_data):
    """Generate a stock price chart using Matplotlib."""
    plt.figure(figsize=(10, 5))
    plt.plot(stock_data["dates"], stock_data["prices"], marker="o", linestyle="-", color="blue", label=symbol)

    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)")
    plt.title(f"Stock Price Trend for {symbol}")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    chart_path = f"{symbol}_chart.png"
    plt.savefig(chart_path, bbox_inches="tight")
    plt.close()

    return chart_path

def stock_chart_handler(update: Update, context: CallbackContext):
    """Telegram command handler for generating stock charts."""
    if len(context.args) < 1:
        update.message.reply_text("⚡ Usage: /chart <stock_symbol> [days]\nExample: /chart TSLA 30")
        return

    symbol = context.args[0].upper()
    days = int(context.args[1]) if len(context.args) > 1 else 30  # Default to 30 days
    api_key = context.bot.data["ALPHA_VANTAGE_API_KEY"]

    stock_data = get_stock_history(symbol, api_key, days)
    if not stock_data:
        update.message.reply_text("⚠️ Unable to fetch stock data. Please try again.")
        return

    chart_path = generate_stock_chart(symbol, stock_data)
    
    with open(chart_path, "rb") as chart_file:
        update.message.reply_photo(photo=chart_file, caption=f"📊 Stock Chart for {symbol} ({days} days)")

    os.remove(chart_path)  # Clean up generated image
