import os
import re

# Directory where message files are stored
MESSAGES_DIR = "messages"

# Expected placeholders for each file
EXPECTED_PLACEHOLDERS = {
    "start.txt": [],
    "set_threshold.txt": ["{percentage}"],
    "set_timeframe.txt": ["{hours}"],
    "add.txt": ["{symbol}"],
    "remove.txt": ["{symbol}"],
    "list.txt": ["{symbols}"],
    "price_change_alert.txt": ["{symbol}", "{percentage}", "{hours}", "{current_price}", "{previous_price}"],
    "help.txt": [],
    "status.txt": ["{symbols}", "{timeframe}", "{threshold}"],
}

# Regex to find placeholders in text
PLACEHOLDER_PATTERN = re.compile(r"\{[a-zA-Z_]+\}")

def validate_placeholders():
    all_valid = True

    for filename, expected in EXPECTED_PLACEHOLDERS.items():
        filepath = os.path.join(MESSAGES_DIR, filename)

        # Check if file exists
        if not os.path.isfile(filepath):
            print(f"❌ Error: {filename} is missing.")
            all_valid = False
            continue

        # Read file content
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        # Find all placeholders in the file
        found_placeholders = PLACEHOLDER_PATTERN.findall(content)

        # Check for missing placeholders
        missing_placeholders = [p for p in expected if p not in found_placeholders]
        if missing_placeholders:
            print(f"❌ Error in {filename}: Missing placeholders: {', '.join(missing_placeholders)}")
            all_valid = False

        # Check for unexpected placeholders
        unexpected_placeholders = [p for p in found_placeholders if p not in expected]
        if unexpected_placeholders:
            print(f"❌ Error in {filename}: Unexpected placeholders: {', '.join(unexpected_placeholders)}")
            all_valid = False

    if all_valid:
        print("✅ All message files have valid placeholders.")
        return True


if __name__ == "__main__":
    validate_placeholders()
