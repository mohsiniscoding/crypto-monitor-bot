from telegram import Update
from telegram.ext import ContextTypes
from utils.validate_whitelist import check_whitelist
from database.db import save_timeframe, load_timeframe

async def set_timeframe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /set_timeframe command."""
    user_id = update.effective_user.id

    if not await check_whitelist(user_id):
        await update.message.reply_text("❌ Access denied. You are not authorized to use this bot.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Please provide a valid timeframe in hours (e.g., /set_timeframe 1).")
        return

    try:
        hours = int(context.args[0])
        if hours < 1 or hours > 24:
            await update.message.reply_text("⚠️ Please provide a valid timeframe in hours (1 - 24).")
            return

        # Save the new timeframe to the database
        save_timeframe(hours)

        # Load message template
        with open("messages/set_timeframe.txt", "r", encoding="utf-8") as file:
            message = file.read()
        await update.message.reply_text(message.format(hours=hours))

    except (ValueError, IndexError):
        await update.message.reply_text("⚠️ Please provide a valid timeframe in hours (e.g., /set_timeframe 1).")
