from telegram import Update
from telegram.ext import ContextTypes
from utils.validate_whitelist import check_whitelist

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    user_id = update.effective_user.id

    if not await check_whitelist(user_id):
        message = (
            f"❌ Access denied. You are not authorized to use this bot.\n\n"
            f"Please ask the bot admin to add your user ID to the whitelist.\n"
            f"Your user ID is: {user_id}\n\n"
            "Once your ID is added, you can rerun the /start command."
        )
        await update.message.reply_text(message)
        return

    # Load message template
    with open("messages/start.txt", "r", encoding="utf-8") as file:
        message = file.read()
    await update.message.reply_text(message)
