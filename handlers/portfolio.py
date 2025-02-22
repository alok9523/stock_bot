import json
import os
import requests
from telegram import Update
from telegram.ext import CallbackContext

# File to store user portfolios
PORTFOLIO_FILE = "user_portfolios.json"
BASE_URL = "https://www.alphavantage.co/query"

# Load or initialize portfolio data
def load_portfolios():
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, "r") as f:
            return json.load(f)
    return {}

def save_portfolios(portfolios):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolios, f, indent=4)

def get_stock_price(symbol: str, api_key: str):
    """Fetch the latest stock price."""
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
        return f"{symbol.upper()}: ${latest_data['1. open']}"
    else:
        return f"{symbol.upper()}: ⚠️ Data unavailable"

def add_stock(update: Update, context: CallbackContext):
    """Adds a stock to the user's portfolio."""
    if not context.args:
        update.message.reply_text("⚡ Usage: /add_stock <stock_symbol>\nExample: /add_stock TSLA")
        return

    user_id = str(update.message.chat_id)
    symbol = context.args[0].upper()

    portfolios = load_portfolios()
    if user_id not in portfolios:
        portfolios[user_id] = []

    if symbol not in portfolios[user_id]:
        portfolios[user_id].append(symbol)
        save_portfolios(portfolios)
        update.message.reply_text(f"✅ {symbol} added to your portfolio!")
    else:
        update.message.reply_text(f"⚠️ {symbol} is already in your portfolio.")

def remove_stock(update: Update, context: CallbackContext):
    """Removes a stock from the user's portfolio."""
    if not context.args:
        update.message.reply_text("⚡ Usage: /remove_stock <stock_symbol>\nExample: /remove_stock TSLA")
        return

    user_id = str(update.message.chat_id)
    symbol = context.args[0].upper()

    portfolios = load_portfolios()
    if user_id in portfolios and symbol in portfolios[user_id]:
        portfolios[user_id].remove(symbol)
        save_portfolios(portfolios)
        update.message.reply_text(f"❌ {symbol} removed from your portfolio.")
    else:
        update.message.reply_text(f"⚠️ {symbol} is not in your portfolio.")

def view_portfolio(update: Update, context: CallbackContext):
    """Displays the user's portfolio with current prices."""
    user_id = str(update.message.chat_id)
    portfolios = load_portfolios()
    api_key = context.bot.data["ALPHA_VANTAGE_API_KEY"]

    if user_id in portfolios and portfolios[user_id]:
        stock_prices = [get_stock_price(symbol, api_key) for symbol in portfolios[user_id]]
        message = "📊 Your Portfolio:\n" + "\n".join(stock_prices)
    else:
        message = "⚠️ Your portfolio is empty. Use /add_stock <symbol> to add stocks."

    update.message.reply_text(message)
