import logging
import asyncio
import aiohttp
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read sensitive data from environment variables
TOKEN = os.getenv("TOKEN")  # Telegram Bot Token
CHAT_ID = os.getenv("CHAT_ID")  # Telegram Chat ID

# Verify environment variables
if not TOKEN or not CHAT_ID:
    raise EnvironmentError("TOKEN or CHAT_ID is missing in .env file.")

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Store the last known state and message_id
last_known_state = None
last_message_id = None

# Ask for the node address
node_address = input("Enter the node address (e.g., 'b8bsblkir41dafs9bwrzbgux3jlusaqmuh5xfndiydbz'): ")

API_URL = f'https://{node_address}.node.k8s.prd.nos.ci/node/info'

# Function to send message via Telegram
async def send_message_async(message):
    """Send a message via Telegram bot."""
    global last_message_id
    try:
        async with aiohttp.ClientSession() as session:
            url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
            params = {
                'chat_id': CHAT_ID,
                'text': message,
                'parse_mode': 'Markdown'
            }
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                result = await response.json()
                last_message_id = result['result']['message_id']  # Store the message ID
                logger.debug(f"Telegram response: {result}")  # Log the Telegram response
                logger.debug(f"Message sent: {message}")
    except Exception as e:
        logger.error(f"Failed to send message: {e}")

# Function to edit a message via Telegram
async def edit_message_async(message):
    """Edit a previously sent message."""
    global last_message_id
    try:
        async with aiohttp.ClientSession() as session:
            url = f'https://api.telegram.org/bot{TOKEN}/editMessageText'
            params = {
                'chat_id': CHAT_ID,
                'message_id': last_message_id,
                'text': message,
                'parse_mode': 'Markdown'
            }
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                result = await response.json()
                logger.debug(f"Telegram response: {result}")  # Log the Telegram response
                logger.debug(f"Message edited: {message}")
    except Exception as e:
        logger.error(f"Failed to edit message: {e}")

# Monitor the API for state changes
async def monitor_api():
    """Check the API for the current state."""
    logger.debug("Checking API...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as response:
                response.raise_for_status()
                data = await response.json()
                logger.debug(f"API Response: {data}")  # Log the full response
                state = data.get('state', 'UNKNOWN')
                uptime_str = data.get('uptime', 'UNKNOWN')
                return state, uptime_str
    except aiohttp.ClientError as e:
        logger.error(f"Error checking API: {e}")
        return "ERROR", None

# Function to calculate uptime
def calculate_uptime(uptime_str):
    """Calculate and return uptime in a readable format."""
    try:
        uptime_time = datetime.strptime(uptime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        now = datetime.utcnow()
        delta = now - uptime_time
        return str(delta).split('.')[0]  # Return the uptime in 'days, hours:minutes:seconds' format
    except ValueError:
        return "Invalid uptime format"

# Send the current node state to Telegram
async def send_current_node_state():
    """Send a message with the current node state or error."""
    global last_known_state
    state, uptime_str = await monitor_api()
    
    
    uptime = calculate_uptime(uptime_str) if uptime_str else "Unknown"
  
    display_state = "JOB/OTHER" if state == "OTHER" else state
  
    if state == "ERROR":
        message = (
            f"⚠️ *Node Status Alert!*\n"
            f"💻 *Node:* `{node_address}`\n"
            f"❌ *Status:* API is not responding.\n"
            f"🛠 Please check the node for issues!"
        )
        await send_message_async(message)
    elif state != last_known_state:
        message = (
            f"🔄 *Node State Change Detected!*\n"
            f"💻 *Node:* `{node_address}`\n"
            f"🌐 *New State:* `{display_state}`\n"
            f"🕒 *Uptime:* `{uptime}`\n"
            f"🚀 *Status updated successfully!*"
        )
        await send_message_async(message)
    else:
        
        message = (
            f"⏳ *Node Status Update:*\n"
            f"💻 *Node:* `{node_address}`\n"
            f"🌐 *State:* `{display_state}`\n"
            f"🕒 *Uptime:* `{uptime}`\n"
            f"📈 Monitoring continues!"
        )
        if last_message_id:
            await edit_message_async(message)
        else:
            await send_message_async(message)
    
    
    last_known_state = state
    logger.debug(f"Last known state updated to: {last_known_state}")


async def send_initial_message():
    """Send a message indicating that the API is now running."""
    message = (
        f"🚀 *Node Monitor Activated!*\n"
        f"💻 *Monitoring Node:* `{node_address}`\n"
        f"📡 *System checks running every 30 seconds.*"
    )
    await send_message_async(message)


def job():
    """Scheduled job to monitor the API state."""
    asyncio.run(send_current_node_state())

# Schedule the job to run every 30 seconds
schedule.every(30).seconds.do(job)


asyncio.run(send_initial_message())


while True:
    schedule.run_pending()
    time.sleep(1)
