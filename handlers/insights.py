import requests
import os

# Load Alpha Vantage API key from config
from config import ALPHA_VANTAGE_API_KEY

BASE_URL = "https://www.alphavantage.co/query"

def get_insights(symbol):
    """
    Fetch stock insights based on RSI, MACD, SMA, and EMA indicators.
    """
    try:
        # Fetch RSI
        rsi_url = f"{BASE_URL}?function=RSI&symbol={symbol}&interval=daily&time_period=14&series_type=close&apikey={ALPHA_VANTAGE_API_KEY}"
        rsi_data = requests.get(rsi_url).json()
        latest_rsi = float(list(rsi_data["Technical Analysis: RSI"].values())[0]["RSI"])

        # Fetch MACD
        macd_url = f"{BASE_URL}?function=MACD&symbol={symbol}&interval=daily&series_type=close&apikey={ALPHA_VANTAGE_API_KEY}"
        macd_data = requests.get(macd_url).json()
        latest_macd = float(list(macd_data["Technical Analysis: MACD"].values())[0]["MACD"])
        macd_signal = float(list(macd_data["Technical Analysis: MACD"].values())[0]["MACD_Signal"])

        # Fetch SMA
        sma_url = f"{BASE_URL}?function=SMA&symbol={symbol}&interval=daily&time_period=50&series_type=close&apikey={ALPHA_VANTAGE_API_KEY}"
        sma_data = requests.get(sma_url).json()
        latest_sma = float(list(sma_data["Technical Analysis: SMA"].values())[0]["SMA"])

        # Generate Insights
        insights = f"📊 **Stock Insights for {symbol.upper()}**\n"
        insights += f"🔹 RSI: {latest_rsi:.2f} ({'Overbought' if latest_rsi > 70 else 'Oversold' if latest_rsi < 30 else 'Neutral'})\n"
        insights += f"🔹 SMA (50-day): {latest_sma:.2f}\n"
        insights += "📢 *Summary:* "

        if latest_rsi > 70 and latest_macd > macd_signal:
            insights += "Stock might be **overbought**, consider selling. 📉"
        elif latest_rsi < 30 and latest_macd < macd_signal:
            insights += "Stock might be **oversold**, could be a buying opportunity. 📈"
        else:
            insights += "Market is neutral, trade with caution. ⚖️"

        return insights

    except Exception as e:
        return f"⚠️ Error fetching insights: {str(e)}"
from telegram import Update
from telegram.ext import CallbackContext

def stock_insights_handler(update: Update, context: CallbackContext):
    """Handles /insights command"""
    if not context.args:
        update.message.reply_text("⚠️ Please provide a stock symbol. Example: `/insights AAPL`")
        return

    symbol = context.args[0].upper()
    insights = get_insights(symbol)  # Ensure get_insights is correctly defined
    update.message.reply_text(insights)
