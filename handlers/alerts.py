# alerts.py
from telegram import Update
from telegram.ext import CallbackContext

user_alerts = {}

def set_alert(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 2:
        update.message.reply_text('Usage: /set_alert <symbol> <price_threshold>')
        return
    
    symbol = context.args[0].upper()
    price_threshold = float(context.args[1])
    
    user_alerts[update.effective_user.id] = (symbol, price_threshold)
    update.message.reply_text(f'Alert set for {symbol} at price {price_threshold}')

def check_alerts(symbol, current_price):
    for user_id, (alert_symbol, threshold) in user_alerts.items():
        if symbol == alert_symbol and current_price >= threshold:
            # Here you would typically send a message to the user
            # However, for brevity, we will just print
            print(f'Sending alert to user {user_id} for {alert_symbol} at price {current_price}')
