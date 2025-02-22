# news.py
import requests
from telegram import Update
from telegram.ext import CallbackContext
import config  # Import your config file

def fetch_stock_news(update: Update, context: CallbackContext) -> None:
    url = f'https://newsapi.org/v2/everything?q=stocks&apiKey={config.NEWS_API_KEY}'
    
    response = requests.get(url)
    data = response.json()
    
    if data.get("articles"):
        news = data['articles'][:5]  # Fetch top 5 articles
        news_messages = "\n\n".join([f"{article['title']} - {article['url']}" for article in news])
        update.message.reply_text(f'Latest Stock News:\n\n{news_messages}')
    else:
        update.message.reply_text('Could not retrieve news articles.')
