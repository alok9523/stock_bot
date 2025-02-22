import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from handlers.market_data import get_stock_price
from handlers.alerts import set_alert, check_alerts
from handlers.news import fetch_stock_news
from handlers.insights import stock_insights
from handlers.charts import get_stock_chart
from config import TOKEN  # Import the TOKEN from config.py

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a function to start the bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Stock Bot! Use /price, /set_alert, /news, /insights, or /chart.")

# Define a function to handle unknown commands
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry, I didn't understand that command.")

# Main function to run the bot
def main() -> None:
    # Use the imported TOKEN instead of hardcoding it
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("price", get_stock_price))
    dispatcher.add_handler(CommandHandler("set_alert", set_alert))
    dispatcher.add_handler(CommandHandler("news", fetch_stock_news))
    dispatcher.add_handler(CommandHandler("insights", stock_insights))
    dispatcher.add_handler(CommandHandler("chart", get_stock_chart))

    # Handler for unknown commands
    dispatcher.add_handler(CommandHandler("unknown", unknown))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
