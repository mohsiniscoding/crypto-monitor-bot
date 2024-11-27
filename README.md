# Crypto Monitor Bot Setup Guide

## Features
- Monitor cryptocurrency prices in real-time.
- Set up alerts for price changes.
- Setup thresholds for alerts.
- Set time intervals for price updates.

This guide provides step-by-step instructions to set up the Crypto Tracker Bot. Follow these steps to install Python, set up a virtual environment, configure environment variables, and prepare your bot for operation.

## Step 1: Installing Python

### Windows
1. Download the latest Python installer from the [official Python website](https://www.python.org/downloads/).
2. Run the installer and ensure you check the box that says "Add Python to PATH".
3. Follow the installation instructions.

### macOS
1. Open Terminal.
2. Install Homebrew if you haven't already:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Python using Homebrew:
   ```bash
   brew install python
   ```

### Linux
1. Open Terminal.
2. Update package lists:
   ```bash
   sudo apt update
   ```
3. Install Python:
   ```bash
   sudo apt install python3
   ```

## Step 2: Set Up Virtual Environment

1. Navigate to your project directory:
   ```bash
   cd /path/to/your/project
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   - **Windows:**
     ```bash
     .\venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```
4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Step 3: Configure Environment Variables

### Step 3.1: Create Bot and Set Up Token

1. Create a bot on your desired platform (e.g., Telegram).
2. Obtain the bot token from the platform.
3. Create a `.env` file in your project directory and add the following line:
   ```plaintext
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```

### Step 3.2: Get ByBit API Credentials

1. Sign up or log in to your ByBit account.
2. Navigate to the API management section and create a new API key.
3. Add the following lines to your `.env` file:
   ```plaintext
   API_KEY=your_api_key_here
   API_SECRET=your_api_secret_here
   ```

## Step 4: Handle Initial Bot Error

1. Start the bot by running your bot script. python3 bot.py
2. On the first `/start`, the bot will throw an error with a user ID.
3. Copy the user ID from the error message.
4. Add the user ID to your whitelist configuration.

## Step 5: Add Valid Symbols

1. Identify the valid symbols you wish to use with your bot.
2. Update the "database/data/valid_symbols.txt" with these valid symbols.

## Step 6: Edit Messages

1. Navigate to the `messages` folder in your project directory.
2. Edit the message files as needed to customize the bot's responses.

---

By following these steps, you should have a fully functional setup for your bot. If you encounter any issues, feel free to reach out on mohsin.io. Happy botting!
```
