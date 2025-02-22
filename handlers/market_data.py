# market_data.py
import requests
from telegram import Update
from telegram.ext import CallbackContext
import config  # Import your config file

def get_stock_price(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        update.message.reply_text('Please provide a stock symbol. Usage: /price <symbol>')
        return
    
    symbol = context.args[0].upper()
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={config.ALPHA_VANTAGE_API_KEY}'
    
    response = requests.get(url)
    data = response.json()
    
    if 'Time Series (5min)' in data:
        last_refreshed = next(iter(data['Time Series (5min)']))
        stock_info = data['Time Series (5min)'][last_refreshed]
        price = stock_info['1. open']
        update.message.reply_text(f'The current price of {symbol} is {price}')
    else:
        update.message.reply_text('Could not retrieve data. Please check the stock symbol.')
