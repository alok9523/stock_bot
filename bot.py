import logging
import json
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from config import TELEGRAM_BOT_TOKEN, ALPHA_VANTAGE_API_KEY, GPT4O_API_KEY
from handlers.market_data import stock_price_handler
from handlers.portfolio import add_stock, remove_stock, view_portfolio
from handlers.alerts import set_alert, remove_alert, view_alerts, start_alert_checker
from handlers.news import stock_news_handler
from handlers.insights import stock_insights_handler
from handlers.charts import generate_stock_chart_handler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load API keys into bot data
def load_bot_data(bot: Bot):
    bot.data = {
        "ALPHA_VANTAGE_API_KEY": ALPHA_VANTAGE_API_KEY,
        "GPT4O_API_KEY": GPT4O_API_KEY,
    }

def start(update: Update, context: CallbackContext):
    """Sends a welcome message when the bot starts."""
    update.message.reply_text(
        "🚀 Welcome to StockBot!\n\n"
        "Use the following commands:\n"
        "📈 /price <symbol> - Get stock price\n"
        "📊 /add_stock <symbol> - Add stock to portfolio\n"
        "📉 /remove_stock <symbol> - Remove stock from portfolio\n"
        "💼 /portfolio - View your portfolio\n"
        "🔔 /set_alert <symbol> <price> - Set stock price alert\n"
        "❌ /remove_alert <symbol> <price> - Remove alert\n"
        "📢 /alerts - View active alerts\n"
        "📰 /news <symbol> - Get stock news\n"
        "🤖 /insights <symbol> - Get AI-powered stock insights\n"
        "📊 /chart <symbol> - Get stock price chart"
    )

def main():
    """Main function to start the bot."""
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    bot = updater.bot
    load_bot_data(bot)

    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("price", stock_price_handler))
    dp.add_handler(CommandHandler("add_stock", add_stock))
    dp.add_handler(CommandHandler("remove_stock", remove_stock))
    dp.add_handler(CommandHandler("portfolio", view_portfolio))
    dp.add_handler(CommandHandler("set_alert", set_alert))
    dp.add_handler(CommandHandler("remove_alert", remove_alert))
    dp.add_handler(CommandHandler("alerts", view_alerts))
    dp.add_handler(CommandHandler("news", stock_news_handler))
    dp.add_handler(CommandHandler("insights", stock_insights_handler))
    dp.add_handler(CommandHandler("chart", generate_stock_chart_handler))

    # Start alert checker in a background thread
    start_alert_checker(bot, ALPHA_VANTAGE_API_KEY)

    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
