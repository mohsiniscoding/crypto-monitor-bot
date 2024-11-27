WHITELIST_FILE_PATH = "whitelist/whitelist-telegram-users.txt"

async def check_whitelist(user_id):
    """
    Check if the user is in the whitelist by reading from the whitelist file.

    :param user_id: The user ID to check
    :return: True if the user is whitelisted, False otherwise
    """
    try:
        with open(WHITELIST_FILE_PATH, "r") as file:
            # Read all lines in the file and strip any leading/trailing whitespace
            whitelisted_ids = [line.strip() for line in file.readlines()]
        
        # Check if the user_id is in the list of whitelisted user IDs
        if str(user_id) in whitelisted_ids:
            return True
        return False
    except FileNotFoundError:
        # If the file is not found, log the error (you can also raise an exception)
        print(f"Whitelist file not found: {WHITELIST_FILE_PATH}")
        return False
    except Exception as e:
        # Catch any other exceptions and log them
        print(f"Error reading the whitelist file: {e}")
        return False

def get_whitelisted_users():
    """
    Get a list of whitelisted user IDs from the whitelist file.

    :return: A list of whitelisted user IDs
    """
    try:
        with open(WHITELIST_FILE_PATH, "r") as file:
            whitelisted_ids = [line.strip() for line in file.readlines()]
        return whitelisted_ids
    except FileNotFoundError:
        print(f"Whitelist file not found: {WHITELIST_FILE_PATH}")
        return []
    except Exception as e:
        print(f"Error reading the whitelist file: {e}")
        return []