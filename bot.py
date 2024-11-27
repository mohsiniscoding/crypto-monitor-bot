import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from commands.start import start
from commands.add import add
from commands.remove import remove
from commands.set_threshold import set_threshold
from commands.set_timeframe import set_timeframe
from commands.list import list_symbols
from commands.help import help_command
from commands.status import status
from utils.validate_placeholders import validate_placeholders
from utils.price_monitoring import monitor_prices

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Validate placeholders before starting the bot
    if not validate_placeholders():
        logger.error("❌ Invalid placeholders found in message templates.")
        raise RuntimeError("One or more message templates have invalid placeholders. Fix them before running the bot.")

    # Get the bot token from the environment variables
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        logger.error("❌ No TELEGRAM_BOT_TOKEN found in .env file.")
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required.")

    # Initialize the bot
    application = ApplicationBuilder().token(bot_token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("remove", remove))
    application.add_handler(CommandHandler("set_threshold", set_threshold))
    application.add_handler(CommandHandler("set_timeframe", set_timeframe))
    application.add_handler(CommandHandler("list", list_symbols))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))

    # Schedule the price monitoring task
    job_queue = application.job_queue
    job_queue.run_repeating(monitor_prices, interval=60, first=0)

    # Log that the bot is running
    logger.info("Bot is running...")

    # Start polling for updates
    application.run_polling()
