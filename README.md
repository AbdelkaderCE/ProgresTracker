# ProgresTracker

A simple Telegram bot that checks whether the **Progres (Webetu)** system is online or down, and sends alerts to Telegram groups.  
Useful for Algerian students who want to know when they can access the Progres platform.

## Features

- Periodically checks `Progres (Webetu) API`.
- Notifies Telegram groups if the site is down or back online.
- Lightweight and easy to deploy.

## Modifications Made

This is a modified version of an open-source bot originally created by **[@0xcyborg](https://github.com/0xcyborg)**.  
The original code can be found [here](https://github.com/0xcyborg/ProgresMonitor).

Changes in this version:
- Removed topic/thread support for simplicity.
- Used English notification messages.
- Slightly optimized message logging and code readability.
- Tailored for general Telegram groups instead of topic-based bots.

## How to Use

1. Add your **Telegram bot token**.
2. Add your **Telegram group ID(s)**.
3. Run the script using Python.

```bash
python3 ProgresTracker.py
