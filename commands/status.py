from telegram import Update
from telegram.ext import ContextTypes
from utils.validate_whitelist import check_whitelist
from database.db import load_tracking_symbols, load_timeframe, load_threshold

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /status command."""
    user_id = update.effective_user.id

    if not await check_whitelist(user_id):
        await update.message.reply_text("❌ Access denied. You are not authorized to use this bot.")
        return

    # Load current tracking symbols, timeframe, and threshold
    current_symbols = load_tracking_symbols()
    current_timeframe = load_timeframe()
    current_threshold = load_threshold()

    with open("messages/status.txt", "r", encoding="utf-8") as file:
        message_template = file.read()

    message = message_template.format(
        symbols=', '.join(current_symbols) if current_symbols else 'None',
        timeframe=current_timeframe,
        threshold=current_threshold
    )

    await update.message.reply_text(message)
