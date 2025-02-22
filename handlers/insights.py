import requests
from config import ALPHA_VANTAGE_API_KEY, POLYGON_API_KEY
from telegram import Update
from telegram.ext import CallbackContext

ALPHA_BASE_URL = "https://www.alphavantage.co/query"
POLYGON_BASE_URL = "https://api.polygon.io/v2"


def get_alpha_insights(symbol):
    """Fetch insights from Alpha Vantage (RSI, MACD, SMA)"""
    try:
        # Fetch RSI
        rsi_url = f"{ALPHA_BASE_URL}?function=RSI&symbol={symbol}&interval=daily&time_period=14&series_type=close&apikey={ALPHA_VANTAGE_API_KEY}"
        rsi_data = requests.get(rsi_url).json()
        print("RSI Data:", rsi_data)  # Debugging

        if "Technical Analysis: RSI" not in rsi_data:
            return None, None, None, None

        latest_date = max(rsi_data["Technical Analysis: RSI"].keys())  
        latest_rsi = float(rsi_data["Technical Analysis: RSI"][latest_date]["RSI"])

        # Fetch MACD
        macd_url = f"{ALPHA_BASE_URL}?function=MACD&symbol={symbol}&interval=daily&series_type=close&apikey={ALPHA_VANTAGE_API_KEY}"
        macd_data = requests.get(macd_url).json()
        print("MACD Data:", macd_data)  # Debugging

        if "Technical Analysis: MACD" not in macd_data:
            return None, None, None, None

        latest_date = max(macd_data["Technical Analysis: MACD"].keys())  
        latest_macd = float(macd_data["Technical Analysis: MACD"][latest_date]["MACD"])  
        macd_signal = float(macd_data["Technical Analysis: MACD"][latest_date]["MACD_Signal"])

        # Fetch SMA
        sma_url = f"{ALPHA_BASE_URL}?function=SMA&symbol={symbol}&interval=daily&time_period=50&series_type=close&apikey={ALPHA_VANTAGE_API_KEY}"
        sma_data = requests.get(sma_url).json()
        print("SMA Data:", sma_data)  # Debugging

        if "Technical Analysis: SMA" not in sma_data:
            return None, None, None, None

        latest_date = max(sma_data["Technical Analysis: SMA"].keys())  
        latest_sma = float(sma_data["Technical Analysis: SMA"][latest_date]["SMA"])

        return latest_rsi, latest_macd, macd_signal, latest_sma

    except Exception as e:
        print("Alpha Vantage Error:", str(e))  # Debugging
        return None, None, None, None


def get_polygon_insights(symbol):
    """Fetch real-time price and volume from Polygon"""
    try:
        url = f"{POLYGON_BASE_URL}/aggs/ticker/{symbol}/prev?apiKey={POLYGON_API_KEY}"
        data = requests.get(url).json()
        print("Polygon Data:", data)  # Debugging

        if "results" not in data or not data["results"]:
            return None, None

        latest_close = data['results'][0]['c']
        latest_volume = data['results'][0]['v']

        return latest_close, latest_volume

    except Exception as e:
        print("Polygon API Error:", str(e))  # Debugging
        return None, None


def stock_insights_handler(update: Update, context: CallbackContext):
    """Handles the /insights command by fetching and replying with stock insights."""
    if not context.args:
        update.message.reply_text("⚠️ Please provide a stock symbol. Example: `/insights AAPL`")
        return

    symbol = context.args[0].upper()
    rsi, macd, macd_signal, sma = get_alpha_insights(symbol)
    close_price, volume = get_polygon_insights(symbol)

    if rsi is None or macd is None or macd_signal is None or sma is None or close_price is None or volume is None:
        update.message.reply_text(f"⚠️ Error fetching insights for {symbol}.")
        return

    insights_message = (
        f"📊 **Stock Insights for {symbol}**\n\n"
        f"🔹 RSI: {rsi:.2f}\n"
        f"🔹 MACD: {macd:.2f} (Signal: {macd_signal:.2f})\n"
        f"🔹 50-day SMA: {sma:.2f}\n"
        f"💰 Close Price: {close_price:.2f}\n"
        f"📈 Volume: {volume:,}"
    )

    update.message.reply_text(insights_message, parse_mode="Markdown")
