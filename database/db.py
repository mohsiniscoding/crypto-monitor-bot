import os

DATABASE_FOLDER = os.path.join(os.path.dirname(__file__), "data")

# File paths for tracking symbols, threshold, and timeframe
SYMBOLS_FILE = os.path.join(DATABASE_FOLDER, "tracking_symbols.txt")
VALID_SYMBOLS_FILE = os.path.join(DATABASE_FOLDER, "valid_symbols.txt")
THRESHOLD_FILE = os.path.join(DATABASE_FOLDER, "current_threshold.txt")
TIMEFRAME_FILE = os.path.join(DATABASE_FOLDER, "current_timeframe.txt")

# Helper functions to load and save data

def load_tracking_symbols():
    """Load the tracking symbols from the database file."""
    try:
        with open(SYMBOLS_FILE, "r") as file:
            return file.read().splitlines()  # Read all lines and split into a list
    except FileNotFoundError:
        return []  # Return empty list if file doesn't exist

def save_tracking_symbols(symbols):
    """Save the tracking symbols to the database file."""
    with open(SYMBOLS_FILE, "w") as file:
        file.write("\n".join(symbols))  # Join symbols into a single string, each on a new line

def load_threshold():
    """Load the current threshold from the database file."""
    try:
        with open(THRESHOLD_FILE, "r") as file:
            return float(file.read().strip())  # Read the threshold and convert to float
    except (FileNotFoundError, ValueError):
        return 5.0  # Default threshold if file doesn't exist or is invalid

def save_threshold(threshold):
    """Save the threshold to the database file."""
    with open(THRESHOLD_FILE, "w") as file:
        file.write(str(threshold))  # Save the threshold as a string

def load_timeframe():
    """Load the current timeframe from the database file."""
    try:
        with open(TIMEFRAME_FILE, "r") as file:
            return int(file.read().strip())  # Read the timeframe and convert to integer
    except (FileNotFoundError, ValueError):
        return 60  # Default timeframe in minutes if file doesn't exist or is invalid

def save_timeframe(timeframe):
    """Save the timeframe to the database file."""
    with open(TIMEFRAME_FILE, "w") as file:
        file.write(str(timeframe))  # Save the timeframe as a string

def add_symbol(symbol):
    """Add a cryptocurrency symbol to the tracking list."""
    symbols = load_tracking_symbols()
    symbol = symbol.upper()  # Ensure the symbol is in uppercase
    if symbol not in symbols:
        symbols.append(symbol)  # Add the symbol if it's not already in the list
        save_tracking_symbols(symbols)
        return True
    return False

def remove_symbol(symbol):
    """Remove a cryptocurrency symbol from the tracking list."""
    symbols = load_tracking_symbols()
    symbol = symbol.upper()
    if symbol in symbols:
        symbols.remove(symbol)  # Remove the symbol if it exists
        save_tracking_symbols(symbols)
        return True
    return False

def load_valid_symbols():
    """Load the list of valid cryptocurrency symbols."""
    try:
        with open(VALID_SYMBOLS_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []