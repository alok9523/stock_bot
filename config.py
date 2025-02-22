import os
from dotenv import load_dotenv

# Load environment variables from a .env file if available
load_dotenv()

# Telegram Bot API Token
TELEGRAM_BOT_TOKEN = os.getenv("7907208352:AAFgh9uy5iiuDi4CmliD9pAvQjoz9ElxTD4", "your-telegram-bot-token")

# Alpha Vantage API Key (for stock data)
ALPHA_VANTAGE_API_KEY = os.getenv("CCZNJHIZ9JP9NG1A", "your-alpha-vantage-api-key")

# OpenAI GPT-4o API Key (for AI insights)
GPT4O_API_KEY = os.getenv("ddc-0D0phWHsoLGsNgnEJ0U1HTm2W0wZF01hkI1wKBS3ih8KK7EENC", "your-gpt4o-api-key")

# Stock Alerts Check Interval (in seconds)
ALERT_CHECK_INTERVAL = int(os.getenv("ALERT_CHECK_INTERVAL", 60))

# File paths for storing user data
PORTFOLIO_FILE = "user_portfolios.json"
ALERTS_FILE = "stock_alerts.json"
