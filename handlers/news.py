import requests
from telegram import Update
from telegram.ext import CallbackContext

# Alpha Vantage API URL
BASE_URL = "https://www.alphavantage.co/query"

def get_stock_news(symbol: str, api_key: str):
    """Fetch the latest news for a given stock symbol."""
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": symbol.upper(),
        "apikey": api_key
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "feed" in data:
        news_items = data["feed"][:3]  # Get the top 3 news articles
        news_list = [f"📰 *{item['title']}*\n🔗 [Read more]({item['url']})" for item in news_items]
        return "\n\n".join(news_list)
    else:
        return "⚠️ No news found or API limit reached."

def stock_news_handler(update: Update, context: CallbackContext):
    """Telegram command handler for fetching stock news."""
    if not context.args:
        update.message.reply_text("⚡ Usage: /news <stock_symbol>\nExample: /news AAPL")
        return

    symbol = context.args[0]
    api_key = context.bot.data["ALPHA_VANTAGE_API_KEY"]
    result = get_stock_news(symbol, api_key)
    
    update.message.reply_text(result, parse_mode="Markdown", disable_web_page_preview=True)
