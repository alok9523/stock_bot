import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from handlers.market_data import get_stock_price
from handlers.portfolio import view_portfolio
import config  # Import your config file

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to Stock Tracker Bot! Use /price <symbol> for stock prices or /portfolio to manage your stocks.")

def main():
    updater = Updater(config.API_TOKEN)  # Use the token from config.py
    
    # Add command handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("price", get_stock_price))
    dp.add_handler(CommandHandler("portfolio", view_portfolio))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
