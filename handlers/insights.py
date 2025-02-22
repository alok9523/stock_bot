import requests
import openai  # GPT-4o API
from telegram import Update
from telegram.ext import CallbackContext

# Alpha Vantage API URL
BASE_URL = "https://www.alphavantage.co/query"

def get_stock_data(symbol: str, api_key: str):
    """Fetch basic stock data for insights."""
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol.upper(),
        "apikey": api_key
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "Time Series (Daily)" in data:
        latest_date = list(data["Time Series (Daily)"].keys())[0]
        latest_data = data["Time Series (Daily)"][latest_date]
        return {
            "symbol": symbol.upper(),
            "date": latest_date,
            "open": latest_data["1. open"],
            "high": latest_data["2. high"],
            "low": latest_data["3. low"],
            "close": latest_data["4. close"],
            "volume": latest_data["5. volume"]
        }
    else:
        return None

def generate_ai_insight(stock_data, gpt_api_key):
    """Generate AI-powered insights using GPT-4o."""
    prompt = f"""
    Analyze the stock {stock_data['symbol']} based on the latest data:
    - Date: {stock_data['date']}
    - Open Price: {stock_data['open']}
    - High Price: {stock_data['high']}
    - Low Price: {stock_data['low']}
    - Close Price: {stock_data['close']}
    - Volume: {stock_data['volume']}

    Provide insights on:
    - Current market trend
    - Potential opportunities or risks
    - Short-term outlook (1-2 weeks)
    """

    openai.api_key = gpt_api_key
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a financial analyst."},
                  {"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

def stock_insights_handler(update: Update, context: CallbackContext):
    """Telegram command handler for fetching AI-generated stock insights."""
    if not context.args:
        update.message.reply_text("⚡ Usage: /insights <stock_symbol>\nExample: /insights TSLA")
        return

    symbol = context.args[0]
    alpha_key = context.bot.data["ALPHA_VANTAGE_API_KEY"]
    gpt_key = context.bot.data["GPT4O_API_KEY"]

    stock_data = get_stock_data(symbol, alpha_key)
    if not stock_data:
        update.message.reply_text("⚠️ Unable to fetch stock data. Please try again.")
        return

    insight = generate_ai_insight(stock_data, gpt_key)
    update.message.reply_text(f"📊 *AI Insights for {symbol}*\n\n{insight}", parse_mode="Markdown")
