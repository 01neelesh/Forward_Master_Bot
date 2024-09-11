from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters
import re

API_TOKEN = "7401746042:AAHpjGxpP2yMmrbyo8IeS3iK2BvwPRcskec"

# List of group IDs from which to forward messages
source_group_ids = [
    -1495473455,  # 1st Group
    -1728887868,  # 2nd Group
    -1653858095,  # 3rd Group
    -1201665184,   # 4th Group (for testing purposes)
    -4591680278
]

# Target group ID where the messages will be forwarded
TARGET_GROUP_ID = -2223262741  # Change this to your target group ID


async def start(update, context):
    welcome_message = (
        "Hello! Welcome to the bot.\n"
        "Here are the available commands:\n"
        "/start -> Show this welcome message\n"
        "/addgroup <group_id> -> Add a group ID to monitor\n"
        "/info -> Information about this bot\n"
    )
    await update.message.reply_text(welcome_message)


def add_group(update, context):
    if len(source_group_ids) < 5:
        try:
            group_id = int(context.args[0])
            if group_id not in source_group_ids:
                source_group_ids.append(group_id)
                update.message.reply_text(f"Group ID {group_id} added for monitoring.")
            else:
                update.message.reply_text(f"Group ID {group_id} is already added.")
        except (IndexError, ValueError):
            update.message.reply_text("Please provide a valid group ID.")
    else:
        update.message.reply_text("Cannot add more than 5 groups.")

# --- 3. Customize Message Before Forwarding ---
def customize_message(message_text):
    # Modify the message to remove any "forwarded from" headers
    customized_text = message_text
    
    # You can add more customization logic here if needed
    return customized_text

# --- 4. Filter Messages ---
def filter_message(message_text):
    # Filter out messages that contain links
    if "http" in message_text:
        return False
    
    # Custom filter rules can be added here, for example:
    # Only allow messages with specific patterns like stock recommendations
    allowed_patterns = [
        r'BNF \d{5} PE @\d+',  # Pattern like BNF 51400 PE @300
        r'BANKNIFTY \d{5} CE \d+',  # Pattern like BANKNIFTY 50800 CE 280-290
        r'\d+₹ To \d+₹',  # Pattern like 280₹ To 315₹
    ]
    
    for pattern in allowed_patterns:
        if re.search(pattern, message_text):
            return True
    
    # If none of the patterns match, filter the message out
    return False

# --- Message Handler for Forwarding ---
async def forward_message(update, context):
    message = update.message
    if message.chat_id in source_group_ids:
        message_text = message.text or ""
        
        # Apply the filter
        if filter_message(message_text):
            # Customize the message
            customized_text = customize_message(message_text)
            
            # Forward the customized message to the target group
            await context.bot.send_message(chat_id=TARGET_GROUP_ID, text=customized_text)

# --- 5. Info Command ---
async def info(update, context):
   await update.message.reply_text("Visit here : https://www.linkedin.com/in/01neelesh/ ")

# --- 6. Main Function to Run the Bot ---
def main():
    # Create the Application instance (async version of Updater)
    application = Application.builder().token(API_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("info", info))

    # Add message handler to forward messages from the source groups
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, forward_message))

    # Run the bot until Ctrl-C is pressed
    application.run_polling()

if __name__ == "__main__":
    main()