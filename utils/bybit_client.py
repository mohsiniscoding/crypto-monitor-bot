import os
from dotenv import load_dotenv
from pybit.unified_trading import HTTP

# Load environment variables from .env file
load_dotenv()

# Retrieve API credentials and category from environment variables
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
CATEGORY = os.getenv('CATEGORY', 'spot')  # Default to 'spot' if not specified

# Initialize the Bybit client
client = HTTP(api_key=API_KEY, api_secret=API_SECRET, testnet=False)

def get_current_price(symbol):
    """
    Fetch the current price of a given symbol from Bybit.

    :param symbol: The cryptocurrency symbol to fetch the price for (e.g., 'BTCUSDT').
    :return: The current price as a float, or None if the price could not be retrieved.
    """
    try:
        response = client.get_tickers(category=CATEGORY, symbol=symbol)
        if response.get("result"):
            return float(response["result"]["list"][0]["lastPrice"])
        else:
            print(f"Failed to retrieve price for {symbol}. Response: {response}")
            return None
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        return None
