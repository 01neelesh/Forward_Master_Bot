from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters
import re

API_TOKEN = "7401746042:AAHpjGxpP2yMmrbyo8IeS3iK2BvwPRcskec"

# # List of group IDs from which to forward messages
# source_group_ids = [
#     -1495473455,  # 1st Group
#     -1728887868,  # 2nd Group
#     -1653858095,  # 3rd Group
#     -1201665184,   # 4th Group (for testing purposes)
#     -4591680278
# ]

# # Target group ID where the messages will be forwarded
# TARGET_GROUP_ID = -2223262741  # Change this to your target group ID


# async def start(update, context):
#     welcome_message = (
#     """ 
    
#         /start -> Hello! Welcome to the bot.\n Here are the available commands\n
#         /addgroup <group_id> -> Add a group ID to monitor
#         /info -> Information about this bot
#         /HowToUse -> Instructions on how to use this bot

#         """
#     )
#     await update.message.reply_text(welcome_message)


# async def how_to_use(update: Update, context):
#     instructions = (
#         "Here’s how to use the bot:\n"
#         "1. Use /start to get a welcome message.\n"
#         "2. Use /addgroup <group_id> to add a group ID for monitoring. "
#         "The bot will monitor messages from the added group.\n"
#         "3. Messages will be filtered and forwarded to your target group.\n"
#         "4. The bot will filter out messages containing links and other unwanted content.\n"
#         "5. You can forward messages from up to 5 groups.\n"
#         "6. The bot is always monitoring even if you are offline.\n"
#     )
#     await update.message.reply_text(instructions)

# # Command to add a group to the list of monitored groups
# async def add_group(update: Update, context):
#     if len(source_group_ids) < 5:
#         try:
#             group_id = int(context.args[0])
#             if group_id not in source_group_ids:
#                 source_group_ids.append(group_id)
#                 await update.message.reply_text(f"Group ID {group_id} added for monitoring.")
#             else:
#                 await update.message.reply_text(f"Group ID {group_id} is already being monitored.")
#         except (IndexError, ValueError):
#             await update.message.reply_text("Please provide a valid group ID.")
#     else:
#         await update.message.reply_text("Cannot add more than 5 groups.")


# # Customize the message before forwarding
# def customize_message(message_text):
#     # Customize the message if needed (currently, no customization)
#     return message_text


# # Filter messages based on certain criteria
# def filter_message(message_text):
#     # Filter out messages that contain links
#     if "http" in message_text:
#         return False

#     # Allow specific patterns (stock-related messages, for example)
#     allowed_patterns = [
#         r'BNF \d{5} PE @\d+',  # Pattern like BNF 51400 PE @300
#         r'BANKNIFTY \d{5} CE \d+',  # Pattern like BANKNIFTY 50800 CE 280-290
#         r'\d+₹ To \d+₹',  # Pattern like 280₹ To 315₹
#     ]

#     for pattern in allowed_patterns:
#         if re.search(pattern, message_text):
#             return True

#     # If none of the patterns match, filter out the message
#     return False


# # Forward message if it passes the filter
# async def forward_message(update: Update, context):
#     message = update.message
#     if message.chat_id in source_group_ids:
#         message_text = message.text or ""

#         # Apply the filter
#         if filter_message(message_text):
#             # Customize the message
#             customized_text = customize_message(message_text)

#             # Forward the customized message to the target group
#             await context.bot.send_message(chat_id=TARGET_GROUP_ID, text=customized_text)


# # Info command to provide information about the bot
# async def info(update: Update, context):
#     await update.message.reply_text("Visit here: https://www.linkedin.com/in/01neelesh/")


# # Main function to run the bot
# def main():
#     # Create the Application instance
#     application = Application.builder().token(API_TOKEN).build()

#     # Add command handlers
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CommandHandler("HowToUse", how_to_use))
#     application.add_handler(CommandHandler("addgroup", add_group))
#     application.add_handler(CommandHandler("info", info))

#     # Add message handler to forward messages from the source groups
#     application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, forward_message))

#     # Run the bot until Ctrl-C is pressed
#     application.run_polling()


# if __name__ == "__main__":
#     main()



# List of group IDs from which to forward messages (empty initially)
source_group_ids = [
    -1495473455,  # 1st Group
    -1728887868,  # 2nd Group
    -1653858095,  # 3rd Group
    -1201665184,   # 4th Group (for testing purposes)
    -4591680278
]

# Target group ID where the messages will be forwarded
TARGET_GROUP_ID = -2223262741  # Replace with your target group ID


# Start command to show welcome message
async def start(update: Update, context):
    welcome_message = (
        "Hello! Welcome to the bot.\n"
        "Here are the available commands:\n"
        "/start -> Show this welcome message\n"
        "/addgroup -> Add the current group to the list of monitored groups\n"
        "/info -> Information about this bot\n"
        "/HowToUse -> Instructions on how to use this bot"
    )
    await update.message.reply_text(welcome_message)


# /HowToUse command to explain how the bot works
async def how_to_use(update: Update, context):
    instructions = (
        "How to use the bot:\n"
        "1. **Add the bot** to a group where you want it to monitor messages.\n"
        "2. **Use the /addgroup command** from within that group. This command will add the group to the bot’s monitored list.\n"
        "3. **The bot will filter and forward** messages from this group to the target group automatically.\n"
        "4. **You can add up to 5 source groups** for message monitoring.\n"
        "5. The bot filters out links and forwards valid messages based on the allowed patterns."
    )
    await update.message.reply_text(instructions)


# Command to add the current group to the list of monitored groups
async def add_group(update: Update, context):
    group_id = update.message.chat_id

    if group_id not in source_group_ids:
        if len(source_group_ids) < 5:
            source_group_ids.append(group_id)
            await update.message.reply_text(f"Group {group_id} has been added to the monitored list.")
        else:
            await update.message.reply_text("You can monitor up to 5 groups only.")
    else:
        await update.message.reply_text("This group is already being monitored.")


# Customize the message before forwarding
def customize_message(message_text):
    # Customize the message if needed (currently, no customization)
    return message_text


# Filter messages based on certain criteria
def filter_message(message_text):
    # Filter out messages that contain links
    if "http" in message_text:
        return False

    # # Allow specific patterns (stock-related messages, for example)
    # allowed_patterns = [
    #     r'BNF \d{5} PE @\d+',  # Pattern like BNF 51400 PE @300
    #     r'BANKNIFTY \d{5} CE \d+',  # Pattern like BANKNIFTY 50800 CE 280-290
    #     r'\d+₹ To \d+₹',  # Pattern like 280₹ To 315₹
    # ]

    # for pattern in allowed_patterns:
    #     if re.search(pattern, message_text):
    #         return True

    # # If none of the patterns match, filter out the message
    return False


# Forward message if it passes the filter
async def forward_message(update: Update, context):
    message = update.message
    if message.chat_id in source_group_ids:
        message_text = message.text or ""

        # Apply the filter
        if filter_message(message_text):
            # Customize the message
            customized_text = customize_message(message_text)

            # Forward the customized message to the target group
            await context.bot.send_message(chat_id=TARGET_GROUP_ID, text=customized_text)


# Info command to provide information about the bot
async def info(update: Update, context):
    await update.message.reply_text("Visit here: https://www.linkedin.com/in/01neelesh/")


# Main function to run the bot
def main():
    # Create the Application instance
    application = Application.builder().token(API_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("HowToUse", how_to_use))
    application.add_handler(CommandHandler("addgroup", add_group))
    application.add_handler(CommandHandler("info", info))

    # Add message handler to forward messages from the source groups
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, forward_message))

    # Run the bot until Ctrl-C is pressed
    application.run_polling()


if __name__ == "__main__":
    main()