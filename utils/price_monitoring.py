import os
import asyncio
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from utils.bybit_client import get_current_price
from database.db import load_tracking_symbols, load_threshold, load_timeframe
from utils.validate_whitelist import get_whitelisted_users
from telegram import Bot

# Load environment variables from .env file
load_dotenv()

# Retrieve the Telegram bot token from environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is required in the .env file.")

# Initialize the Telegram bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("monitoring.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

# Dictionary to store current prices of symbols
symbol_prices = {}

# Global variable to track the last check time
last_check_time = datetime.now()

async def notify_users(message):
    """Send a notification to all whitelisted users."""
    whitelisted_users = get_whitelisted_users()
    for user_id in whitelisted_users:
        try:
            await bot.send_message(chat_id=user_id, text=message)
            logging.info(f"Sent message to user {user_id}: {message}")
        except Exception as e:
            logging.error(f"Failed to send message to {user_id}: {e}")

async def monitor_prices(context):
    """Monitor price changes and notify users if thresholds are met."""
    global symbol_prices, last_check_time
    symbols = load_tracking_symbols()
    threshold = load_threshold()
    timeframe = load_timeframe()

    logging.info("Starting price monitoring...")

    # Check for new symbols and fetch their initial prices
    for symbol in symbols:
        if symbol not in symbol_prices:
            current_price = get_current_price(symbol)
            if current_price is not None:
                symbol_prices[symbol] = current_price
                logging.info(f"Fetched initial price for {symbol}: {current_price}")
            else:
                error_message = f"⚠️ Error fetching initial price for {symbol}. Please check the symbol or try again later."
                await notify_users(error_message)
                logging.error(error_message)

    logging.info(f"Monitoring {len(symbol_prices)} symbols for price changes...")
    logging.info(f"Threshold: {threshold}%, Timeframe: {timeframe} hours")
    logging.info(f"Last check time: {last_check_time}")
    logging.info(f"Current time: {datetime.now()}")

    # Check if the timeframe is met
    current_time = datetime.now()
    elapsed_time = current_time - last_check_time

    if elapsed_time >= timedelta(hours=timeframe): # TODO: uncomment this line
    # if True: # TODO: remove this line
        logging.info("Timeframe met, checking price changes...")
        # Check price changes for each symbol
        for symbol, previous_price in symbol_prices.items():
            current_price = get_current_price(symbol)
            if current_price is None:
                error_message = f"⚠️ Error fetching current price for {symbol}. Please check the symbol or try again later."
                await notify_users(error_message)
                logging.error(error_message)
                continue

            price_change = ((current_price - previous_price) / previous_price) * 100
            logging.info(f"Price change for {symbol}: {abs(price_change)}%")
            logging.info(f"Previous price: {previous_price} | Current price: {current_price}")

            if abs(price_change) >= threshold:
                logging.info(f"Price change for {symbol}: {price_change:.2f}%")
                message = (
                    f"📈 Price Alert! The price of {symbol} has changed by {price_change:.2f}% in the last {timeframe} hours.\n"
                    f"Current price: {current_price}\nPrevious price: {previous_price}"
                )
                await notify_users(message)
                logging.info(f"Price alert for {symbol}: {message}")

            # Update the stored price
            symbol_prices[symbol] = current_price

        # Update the last check time
        last_check_time = current_time
        logging.info("Price monitoring completed.")
    else:
        logging.info("Timeframe not met, skipping price check.")

async def start_monitoring():
    """Start the price monitoring process."""
    try:
        await monitor_prices()
    except Exception as e:
        logging.error(f"Error in monitoring process: {e}")
        await notify_users(f"⚠️ An error occurred in the monitoring process: {e}")

# Call this function when the bot starts
if __name__ == "__main__":
    asyncio.run(start_monitoring())
