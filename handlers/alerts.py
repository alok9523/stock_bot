import json
import os
import requests
import threading
import time
from telegram import Update
from telegram.ext import CallbackContext

# File to store alerts
ALERTS_FILE = "stock_alerts.json"
BASE_URL = "https://www.alphavantage.co/query"
CHECK_INTERVAL = 60  # Check alerts every 60 seconds

# Load or initialize alerts data
def load_alerts():
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_alerts(alerts):
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f, indent=4)

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
        return float(latest_data["1. open"])
    else:
        return None

def set_alert(update: Update, context: CallbackContext):
    """Sets a stock price alert."""
    if len(context.args) < 2:
        update.message.reply_text("⚡ Usage: /set_alert <symbol> <price>\nExample: /set_alert TSLA 750")
        return

    user_id = str(update.message.chat_id)
    symbol = context.args[0].upper()
    try:
        price = float(context.args[1])
    except ValueError:
        update.message.reply_text("⚠️ Please enter a valid price.")
        return

    alerts = load_alerts()
    if user_id not in alerts:
        alerts[user_id] = []

    alerts[user_id].append({"symbol": symbol, "price": price})
    save_alerts(alerts)
    
    update.message.reply_text(f"🔔 Alert set for {symbol} at ${price}.")

def remove_alert(update: Update, context: CallbackContext):
    """Removes an alert."""
    if len(context.args) < 2:
        update.message.reply_text("⚡ Usage: /remove_alert <symbol> <price>\nExample: /remove_alert TSLA 750")
        return

    user_id = str(update.message.chat_id)
    symbol = context.args[0].upper()
    try:
        price = float(context.args[1])
    except ValueError:
        update.message.reply_text("⚠️ Please enter a valid price.")
        return

    alerts = load_alerts()
    if user_id in alerts:
        alerts[user_id] = [alert for alert in alerts[user_id] if alert["symbol"] != symbol or alert["price"] != price]
        save_alerts(alerts)
        update.message.reply_text(f"❌ Alert removed for {symbol} at ${price}.")
    else:
        update.message.reply_text("⚠️ No matching alert found.")

def view_alerts(update: Update, context: CallbackContext):
    """Displays all active alerts for the user."""
    user_id = str(update.message.chat_id)
    alerts = load_alerts()

    if user_id in alerts and alerts[user_id]:
        alert_list = [f"{alert['symbol']} at ${alert['price']}" for alert in alerts[user_id]]
        message = "📢 Your Active Alerts:\n" + "\n".join(alert_list)
    else:
        message = "⚠️ You have no active alerts."

    update.message.reply_text(message)

def check_alerts(bot, api_key):
    """Checks stock prices and notifies users if an alert is triggered."""
    while True:
        alerts = load_alerts()
        for user_id, user_alerts in alerts.items():
            for alert in user_alerts:
                stock_price = get_stock_price(alert["symbol"], api_key)
                if stock_price and ((alert["price"] <= stock_price) or (alert["price"] >= stock_price)):
                    bot.send_message(chat_id=user_id, text=f"🚨 Alert! {alert['symbol']} has hit ${stock_price}!")
                    user_alerts.remove(alert)

            # Save updated alerts after removing triggered ones
            save_alerts(alerts)
        
        time.sleep(CHECK_INTERVAL)

def start_alert_checker(bot, api_key):
    """Starts the alert checking process in a separate thread."""
    thread = threading.Thread(target=check_alerts, args=(bot, api_key), daemon=True)
    thread.start()
