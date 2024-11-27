from telegram import Update
from telegram.ext import ContextTypes
from utils.validate_whitelist import check_whitelist
from database.db import remove_symbol, load_tracking_symbols, load_valid_symbols

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /remove command."""
    user_id = update.effective_user.id

    if not await check_whitelist(user_id):
        await update.message.reply_text("❌ Access denied. You are not authorized to use this bot.")
        return

    symbol = " ".join(context.args)
    if not symbol:
        await update.message.reply_text("⚠️ Please specify a cryptocurrency symbol to remove (e.g., /remove BTCUSDT).")
        return

    # Load the user's current watchlist and valid symbols
    current_symbols = load_tracking_symbols()
    valid_symbols = load_valid_symbols()

    # Check if the symbol is valid
    if symbol.upper() not in valid_symbols:
        await update.message.reply_text(f"⚠️ The symbol {symbol} is not a valid cryptocurrency symbol.")
        return

    # Check if the symbol exists in the user's watchlist
    if symbol not in current_symbols:
        await update.message.reply_text(f"⚠️ The symbol {symbol} is not in your watchlist.")
        return

    # Remove symbol from user's watchlist in the database
    success = remove_symbol(symbol)
    if not success:
        await update.message.reply_text("⚠️ Failed to remove the symbol from your watchlist. Please try again.")
        return

    with open("messages/remove.txt", "r", encoding="utf-8") as file:
        message = file.read()

    await update.message.reply_text(message.format(symbol=symbol))
