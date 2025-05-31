from time import sleep
from requests import get, exceptions

# --- MAIN CONFIGURATION ---
API_URL = "https://progres.mesrs.dz/api/infos"
BOT_TOKEN = "**"  # <-- PASTE YOUR TELEGRAM BOT TOKEN
GROUPS_IDS = ("****",)  # <-- PASTE YOUR GROUP ID (e.g., "-100...")

# --- PROXY CONFIGURATION (For running on a server outside Algeria) ---
# You need a reliable proxy server located in Algeria for this to work.
# Replace with your actual proxy IP and Port. Leave as None to disable the proxy.
PROXY_IP = "*******"      # e.g., "197.200.10.1" or set to None
PROXY_PORT = "****"   # e.g., "8080" or set to None

# --- SCRIPT SETTINGS ---
# MODIFIED: Updated headers to look like a real browser request. This is more reliable.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
REQUEST_TIMEOUT = 15  # Increased timeout for potentially slower proxy connections
THRESHOLD = 5
LOOP_TIME = 1 # Set to 5 minutes for a more reasonable check interval

def send_message(text):
    """Sends a message to every group ID listed in GROUPS_IDS."""
    print(f"Attempting to send message: {text}")
    try:
        for group_id in GROUPS_IDS:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={group_id}&text={text}&disable_notification=true"
            response = get(url)
            if response.status_code == 200:
                print(f"Sent successfully to Telegram - Group ID: {group_id}")
            else:
                print(f"Telegram returned an error: {response.status_code} for Group ID: {group_id}")
                print(f"Error details: {response.json()}")
            sleep(1)
    except Exception as E:
        print(f"An error occurred in the 'send_message' function: {E}")

# --- MAIN SCRIPT LOGIC ---

send_message("🔆 Bot has been restarted. Starting API monitoring... 🔆")

api_is_up = True
failure_counter = 0

while True:
    # NEW: Logic to prepare the proxy settings for the request
    proxies = None
    if PROXY_IP and PROXY_PORT:
        proxy_url = f"http://{PROXY_IP}:{PROXY_PORT}"
        proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }
        print(f"Checking API via proxy: {PROXY_IP}:{PROXY_PORT}...")
    else:
        print(f"Checking API status at {API_URL} (timeout is {REQUEST_TIMEOUT}s)...")
        
    try:
        # MODIFIED: The get() request now includes the 'proxies' argument.
        get(API_URL, headers=HEADERS, timeout=REQUEST_TIMEOUT, proxies=proxies)
        
        print("API check successful.")
        
        if not api_is_up:
            print("API is back online!")
            send_message("✅ The Progres API is working again. ✅")
            api_is_up = True
        
        failure_counter = 0

    except exceptions.RequestException as e:
        failure_counter += 1
        print(f"API check failed ({failure_counter}/{THRESHOLD}).")
        
        if api_is_up and failure_counter >= THRESHOLD:
            print("API has gone down! Sending alert.")
            send_message("❌ The Progres API seems to be down. ❌")
            api_is_up = False
            
    except Exception as E:
        print(f"An unexpected error occurred in the main loop: {E}")

    print(f"Waiting for {LOOP_TIME} seconds before the next check...")
    sleep(LOOP_TIME)
