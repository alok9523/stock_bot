import requests
from telegram import Update
from telegram.ext import CallbackContext

# Alpha Vantage API URL
BASE_URL = "https://www.alphavantage.co/query"

def get_stock_price(symbol: str, api_key: str):
    """Fetch the latest stock price for a given symbol from Alpha Vantage."""
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol.upper(),
        "interval": "5min",
        "apikey": api_key
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "Time Series (5min)" in data:
        latest_timestamp = list(data["Time Series (5min)"].keys())[0]
        latest_data = data["Time Series (5min)"][latest_timestamp]
        return f"📈 Stock: {symbol.upper()}\n💰 Price: ${latest_data['1. open']}\n📅 Time: {latest_timestamp}"
    else:
        return "⚠️ Invalid stock symbol or API limit reached."

def stock_price_handler(update: Update, context: CallbackContext):
    """Telegram command handler for fetching stock prices."""
    if not context.args:
        update.message.reply_text("⚡ Usage: /price <stock_symbol>\nExample: /price AAPL")
        return

    symbol = context.args[0]
    api_key = context.bot.data["ALPHA_VANTAGE_API_KEY"]  # This will be set in bot.py
    result = get_stock_price(symbol, api_key)
    
    update.message.reply_text(result)
