# Telegram Message Forwarding Bot

## Overview

This Telegram bot is designed to monitor messages from multiple source groups and forward them to a single target group. The bot filters out unwanted content and ensures messages are forwarded according to specified patterns.

## Features

- **Monitor Source Groups**: Add up to 5 source groups.
- **Forward Messages**: Forward messages from source groups to one target group.
- **Filter Messages**: Customize and filter messages before forwarding.
- **Add/Remove Groups**: Manage source and target groups with specific commands.

## Deployment

The bot is currently deployed on PythonAnywhere. To run the bot on your own server, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/telegram-message-bot.git
   cd telegram-message-bot

2. **Install Dependencies**

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows use `venv\Scripts\activate`
    pip install -r requirements.txt

3. **Configure the Bot**

    ```python
    API_TOKEN = "YOUR_BOT_API_TOKEN_HERE"
Replace the API_TOKEN with your own bot token from BotFather in the bot.py file.

