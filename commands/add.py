from telegram import Update
from telegram.ext import ContextTypes
from utils.validate_whitelist import check_whitelist
from database.db import add_symbol, load_tracking_symbols, load_valid_symbols
from utils.bybit_client import get_current_price

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /add command."""
    user_id = update.effective_user.id

    if not await check_whitelist(user_id):
        await update.message.reply_text("❌ Access denied. You are not authorized to use this bot.")
        return

    symbol = " ".join(context.args)
    if not symbol:
        await update.message.reply_text("⚠️ Please specify a cryptocurrency symbol to add (e.g., /add BTCUSDT).")
        return

    # Load the user's current watchlist
    current_symbols = load_tracking_symbols()
    valid_symbols = load_valid_symbols()

    # Check if the symbol is valid
    if symbol.upper() not in valid_symbols:
        message = (
            f"⚠️ Invalid symbol. Please enter a valid cryptocurrency symbol.\n\n"
            f"List of valid symbols:\n"
            f"{', '.join(valid_symbols)}"
        )
        await update.message.reply_text(message)
        return
    
    # Check if the symbol already exists in the user's watchlist
    if symbol in current_symbols:
        await update.message.reply_text(f"⚠️ The symbol {symbol} is already in your watchlist.")
        return

    # Fetch the current price of the symbol
    current_price = get_current_price(symbol)
    if current_price is None:
        await update.message.reply_text(f"⚠️ Failed to retrieve the current price for {symbol}. Please try again.")
        return

    # Add symbol to user's watchlist in the database
    success = add_symbol(symbol)
    if not success:
        await update.message.reply_text("⚠️ Failed to add the symbol to your watchlist. Please try again.")
        return

    with open("messages/add.txt", "r", encoding="utf-8") as file:
        message = file.read()

    # Include the current price in the response message
    await update.message.reply_text(message.format(symbol=symbol) + f"\nCurrent price: {current_price}")
