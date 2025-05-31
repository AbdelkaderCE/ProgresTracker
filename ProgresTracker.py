# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                       #
#                     API Uptime Telegram Bot                           #
#                                                                       #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Description:
# This script continuously monitors a specified API endpoint. It sends a
# notification to a Telegram group if the API status changes from "up" to "down"
# or vice-versa.
#
# How to Configure:
# 1. Fill in the placeholders in the "CONFIGURATION" section below.
# 2. You will need a Telegram Bot Token from @BotFather.
# 3. You will need the Chat ID of your group. You can get this by adding a
#    bot like @RawDataBot to your group and checking the JSON data.
#
# Important Note on API Accessibility:
# This script can only monitor APIs that are publicly accessible from the
# server where the script is running. Some APIs use geoblocking (restricting
# access based on country) or require authentication (like a JWT token).
# If an API uses these security measures, this simple script will not be
# able to access it from a standard international hosting provider.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from time import sleep
from requests import get, exceptions

# --- CONFIGURATION ---
# Fill in these values before running the script.

# The URL of the API you want to monitor.
API_URL = "https://progres.mesrs.dz/api/infos"  # <-- Change this to your target API

# Your Telegram Bot's Token from @BotFather.
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # <-- IMPORTANT: Paste your Bot Token here

# The chat ID(s) of the Telegram group(s) you want to send messages to.
# Group IDs usually start with a hyphen (-).
# To add more than one group, separate them with a comma: ("-100...", "-100...")
GROUPS_IDS = ("YOUR_GROUP_ID_HERE",)  # <-- IMPORTANT: Paste your Group ID here

# How many times the API must fail in a row before sending a "down" alert.
THRESHOLD = 5

# How many seconds to wait between each check.
# A low number like 10 is good for testing. For real use, consider a longer
# time like 300 (5 minutes) or 900 (15 minutes) to avoid making too many requests.
LOOP_TIME = 10
# --- END OF CONFIGURATION ---


def send_message(text):
    """Sends a message to every group ID listed in GROUPS_IDS."""
    print(f"Attempting to send message: {text}")
    try:
        for group_id in GROUPS_IDS:
            # Construct the API URL for sending a message to Telegram
            url = f"httpshttps://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={group_id}&text={text}&disable_notification=true"
            response = get(url)

            if response.status_code == 200:
                print(f"Sent successfully to Telegram - Group ID: {group_id}")
            else:
                print(f"Telegram returned an error: {response.status_code} for Group ID: {group_id}")
                print(f"Error details: {response.json()}")
            
            # Wait 1 second between sending to different groups to avoid rate limits
            sleep(1)
            
    except Exception as e:
        print(f"An error occurred in the 'send_message' function: {e}")


# --- MAIN SCRIPT LOGIC ---

# Send a startup message so you know the bot is running.
send_message("🔆 Bot has been restarted. Starting API monitoring... 🔆")

# We start by assuming the API is down (`api_is_up = False`).
# This forces the bot to send a "working again" message on the very first
# successful check, confirming that it's able to reach the API.
api_is_up = False
failure_counter = 0

while True:
    try:
        # Try to make a request to the target API.
        # We don't need to save the response, just confirm it doesn't error out.
        get(API_URL, timeout=REQUEST_TIMEOUT)
        
        # If the line above runs without an error, the API is considered online.
        print("API check successful.")
        
        # Check if the API was previously considered down.
        if not api_is_up:
            print("API is back online! Sending notification.")
            send_message("✅ The Progres API is working again. ✅")
            # Update the state to 'up' so we don't send this message again.
            api_is_up = True
        
        # Reset the failure counter on any successful check.
        failure_counter = 0

    except exceptions.RequestException as e:
        # This block runs if get() fails (e.g., timeout, connection error).
        failure_counter += 1
        print(f"API check failed ({failure_counter}/{THRESHOLD}).")
        
        # Check if the API was previously 'up' and if we've passed the failure threshold.
        if api_is_up and failure_counter >= THRESHOLD:
            print("API has gone down! Sending alert.")
            send_message("❌ The Progres API seems to be down. ❌")
            # Update the state to 'down' so we don't send this alert again.
            api_is_up = False
            
    except Exception as e:
        print(f"An unexpected error occurred in the main loop: {e}")

    # Wait for the specified time before the next check.
    print(f"Waiting for {LOOP_TIME} seconds before the next check...")
    sleep(LOOP_TIME)
