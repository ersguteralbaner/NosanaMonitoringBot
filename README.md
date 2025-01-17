# Node Monitoring Bot

A Python bot to monitor the state of a Nosana node and send status updates to a Telegram chat. The bot leverages asynchronous programming for efficiency and integrates with the Telegram Bot API for notifications.

## Features
- Tracks node state changes and uptime.
- Sends notifications via Telegram for state updates or errors.
- Uses dynamic message editing to keep Telegram updates clean.
- Runs scheduled checks every 30 seconds.

---

## Prerequisites
- **Python 3.8+** installed on your system.
- **pip** (Python's package manager) available.
- A Telegram Bot Token and Chat ID.

---

## Installation

### Step 1: Clone the Repository
Clone this repository to your local system or create a directory for the script:
```bash
git clone https://github.com/ersguteralbaner/NosanaMonitoringBot.git
cd NosanaMonitoringBot
```

### Step 2: Install Required Dependencies

Install the dependencies using pip:
```bash
pip install aiohttp schedule python-dotenv
```

### Step 3: Set up TelegramBot and Environment Variables

  1. Create a Telegram Bot:

  Open Telegram and search for BotFather.
  Start a chat with BotFather and send the command /newbot.
  Follow the prompts to name your bot and choose a username (e.g., YourBotName_bot).
  After creation, BotFather will give you a token in this format:

    123456789:ABCDEF1234567890abcdef1234567890

  Save this token for later.

    
  2. Get Your Chat ID:

  Start a chat with your bot (search for it by its username).
  Send any message to the bot.
  Use the following API call to get your Chat ID:

    curl https://api.telegram.org/bot<Your Bot Token>/getUpdates

  Look for the chat field in the response. For example:

    {
        "message": {
            "chat": {
                "id": 123456789,
                "type": "private",
                "username": "YourUsername"
            }
        }
    }

  In this example, the Chat ID is 123456789.

  Configure the .env File:

  Edit the .env file in the root of your project:

    nano .env

  Add the following content to your .env file:

    TOKEN=<Your Telegram Bot Token>
    CHAT_ID=<Your Telegram Chat ID>
  Replace <Your Telegram Bot Token> with the token provided by BotFather.
  Replace <Your Telegram Chat ID> with the ID retrieved earlier.

  Save the changes by pressing CTRL+O then ENTER and exit with CTRL+X

### Step 4: Run the script by executing the following command:
```bash
python node_monitor.py
```
When prompted, enter the node address (e.g., b8bsblkir41dafs9bwrzbgux3jlusaqmuh5xfndiydbz). The bot will monitor the provided node and send updates to the specified Telegram chat.


Features and Alerts

  Initial Startup: Sends a message indicating the bot is monitoring the node.
  State Change Detection: Notifies the user whenever the node state changes.
  Error Handling: Alerts the user if the API is unresponsive.
  Uptime Tracking: Displays the current uptime in human-readable format.

Common Issues

  Bot Not Sending Messages: Verify the TOKEN and CHAT_ID in the .env file.
  Environment Variable Errors: Ensure the .env file exists and is correctly configured.
  Node Monitoring Issues: Ensure the node address is valid and the API is reachable.

Preview

![Screenshot from 2025-01-17 09-03-08](https://github.com/user-attachments/assets/c3e5aa20-7591-4222-a36f-73b9050541ed)


