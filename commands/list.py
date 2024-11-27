from telegram import Update
from telegram.ext import ContextTypes
from utils.validate_whitelist import check_whitelist

async def list_symbols(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /list command."""
    user_id = update.effective_user.id

    if not await check_whitelist(user_id):
        await update.message.reply_text("❌ Access denied. You are not authorized to use this bot.")
        return

    # TODO: Retrieve and display the user's watchlist

    with open("messages/list.txt", "r", encoding="utf-8") as file:
        message = file.read()
    await update.message.reply_text(message)
