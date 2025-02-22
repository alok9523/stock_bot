import requests
from config import ALPHA_VANTAGE_API_KEY, POLYGON_API_KEY

ALPHA_BASE_URL = "https://www.alphavantage.co/query"
POLYGON_BASE_URL = "https://api.polygon.io/v2"

def get_alpha_insights(symbol):
    """Fetch insights from Alpha Vantage (RSI, MACD, SMA)"""
    try:
        # Fetch RSI
        rsi_url = f"{ALPHA_BASE_URL}?function=RSI&symbol={symbol}&interval=daily&time_period=14&series_type=close&apikey={ALPHA_VANTAGE_API_KEY}"
        rsi_data = requests.get(rsi_url).json()
        latest_rsi = float(list(rsi_data["Technical Analysis: RSI"].values())[0]["RSI"])

        # Fetch MACD
        macd_url = f"{ALPHA_BASE_URL}?function=MACD&symbol={symbol}&interval=daily&series_type=close&apikey={ALPHA_VANTAGE_API_KEY}"
        macd_data = requests.get(macd_url).json()
        latest_macd = float(list(macd_data["Technical Analysis: MACD"].values())[0]["MACD"])
        macd_signal = float(list(macd_data["Technical Analysis: MACD"].values())[0]["MACD_Signal"])

        # Fetch SMA
        sma_url = f"{ALPHA_BASE_URL}?function=SMA&symbol={symbol}&interval=daily&time_period=50&series_type=close&apikey={ALPHA_VANTAGE_API_KEY}"
        sma_data = requests.get(sma_url).json()
        latest_sma = float(list(sma_data["Technical Analysis: SMA"].values())[0]["SMA"])

        return latest_rsi, latest_macd, macd_signal, latest_sma
    except:
        return None, None, None, None

def get_polygon_insights(symbol):
    """Fetch real-time price and volume from Polygon"""
    try:
        url = f"{POLYGON_BASE_URL}/aggs/ticker/{symbol}/prev?apiKey={POLYGON_API_KEY}"
        data = requests.get(url).json()
        latest_close = data['results'][0]['c']  # Closing price
        latest_volume = data['results'][0]['v']  # Trading volume

        return latest_close, latest_volume
    except:
        return None, None

def get_insights(symbol):
    """Combines Alpha Vantage & Polygon insights"""
    latest_rsi, latest_macd, macd_signal, latest_sma = get_alpha_insights(symbol)
    latest_close, latest_volume = get_polygon_insights(symbol)

    if latest_rsi is None or latest_close is None:
        return f"⚠️ Error fetching insights for {symbol.upper()}."

    insights = f"📊 **Stock Insights for {symbol.upper()}**\n"
    insights += f"🔹 **RSI**: {latest_rsi:.2f} ({'Overbought' if latest_rsi > 70 else 'Oversold' if latest_rsi < 30 else 'Neutral'})\n"
    insights += f"🔹 **MACD**: {latest_macd:.2f} ({'Bullish' if latest_macd > macd_signal else 'Bearish'})\n"
    insights += f"🔹 **SMA (50-day)**: {latest_sma:.2f}\n"
    insights += f"🔹 **Closing Price**: ${latest_close:.2f}\n"
    insights += f"🔹 **Trading Volume**: {latest_volume:,}\n"
    insights += "📢 *Summary:* "

    if latest_rsi > 70 and latest_macd > macd_signal:
        insights += "Stock might be **overbought**, consider selling. 📉"
    elif latest_rsi < 30 and latest_macd < macd_signal:
        insights += "Stock might be **oversold**, could be a buying opportunity. 📈"
    else:
        insights += "Market is neutral, trade with caution. ⚖️"

    return insights
