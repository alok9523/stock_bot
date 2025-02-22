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
        print("RSI Data:", rsi_data)  # Debugging

        if "Technical Analysis: RSI" not in rsi_data:
            return None, None, None, None

        latest_rsi = float(list(rsi_data["Technical Analysis: RSI"].values())[0]["RSI"])

        # Fetch MACD
        macd_url = f"{ALPHA_BASE_URL}?function=MACD&symbol={symbol}&interval=daily&series_type=close&apikey={ALPHA_VANTAGE_API_KEY}"
        macd_data = requests.get(macd_url).json()
        print("MACD Data:", macd_data)  # Debugging

        if "Technical Analysis: MACD" not in macd_data:
            return None, None, None, None

        latest_macd = float(list(macd_data["Technical Analysis: MACD"].values())[0]["MACD"])
        macd_signal = float(list(macd_data["Technical Analysis: MACD"].values())[0]["MACD_Signal"])

        # Fetch SMA
        sma_url = f"{ALPHA_BASE_URL}?function=SMA&symbol={symbol}&interval=daily&time_period=50&series_type=close&apikey={ALPHA_VANTAGE_API_KEY}"
        sma_data = requests.get(sma_url).json()
        print("SMA Data:", sma_data)  # Debugging

        if "Technical Analysis: SMA" not in sma_data:
            return None, None, None, None

        latest_sma = float(list(sma_data["Technical Analysis: SMA"].values())[0]["SMA"])

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

