from telegram import Update
from telegram.ext import ContextTypes
from utils.validate_whitelist import check_whitelist
from database.db import save_threshold, load_threshold

async def set_threshold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /set_threshold command."""
    user_id = update.effective_user.id

    if not await check_whitelist(user_id):
        await update.message.reply_text("❌ Access denied. You are not authorized to use this bot.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Please provide a valid threshold percentage (e.g., /set_threshold 5).")
        return

    try:
        threshold_percentage = float(context.args[0])

        if threshold_percentage <= 0 or threshold_percentage > 100:
            await update.message.reply_text("⚠️ Threshold percentage must be a positive number between 1 and 100. Please try again.")
            return

        # Save the new threshold to the database
        save_threshold(threshold_percentage)

        # Load message template
        with open("messages/set_threshold.txt", "r", encoding="utf-8") as file:
            message = file.read()
        await update.message.reply_text(message.format(percentage=threshold_percentage))

    except (ValueError, IndexError):
        await update.message.reply_text("⚠️ Please provide a valid threshold percentage (e.g., /set_threshold 5).")
