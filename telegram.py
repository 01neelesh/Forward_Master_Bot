from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import re

API_TOKEN = "7401746042:AAHpjGxpP2yMmrbyo8IeS3iK2BvwPRcskec"


# List of group IDs from which to forward messages
source_group_ids = []

# Target group ID where the messages will be forwarded
TARGET_GROUP_ID = -1653858095  # Change this to your target group ID

# Initialize the updater and dispatcher
updater = Updater(token=API_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# --- 1. Start Command ---
def start(update, context):
    welcome_message = (
        "Hello! Welcome to the bot.\n"
        "Here are the available commands:\n"
        "/start -> Show this welcome message\n"
        "/addgroup <group_id> -> Add a group ID to monitor\n"
        "/info -> Information about this bot\n"
    )
    update.message.reply_text(welcome_message)

# --- 2. Add Group Command ---
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
def forward_message(update, context):
    message = update.message
    if message.chat_id in source_group_ids:
        message_text = message.text or ""
        
        # Apply the filter
        if filter_message(message_text):
            # Customize the message
            customized_text = customize_message(message_text)
            
            # Forward the customized message to the target group
            context.bot.send_message(chat_id=TARGET_GROUP_ID, text=customized_text)

# --- 5. Info Command ---
def info(update, context):
    update.message.reply_text("Visit here : https://www.linkedin.com/in/01neelesh/ ")

# --- Add handlers to the dispatcher ---
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("addgroup", add_group, pass_args=True))
dispatcher.add_handler(CommandHandler("info", info))

# Message handler to forward messages from added groups
dispatcher.add_handler(MessageHandler(Filters.text & Filters.chat_type.groups, forward_message))

# Start the bot
updater.start_polling()

# Run the bot until Ctrl-C is pressed
updater.idle()
