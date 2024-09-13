from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import re
import logging

API_TOKEN = "take your own token from botfather"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

source_group_ids = []
TARGET_GROUP_ID = None  # Initialize TARGET_GROUP_ID as None

# Start command to show welcome message
async def start(update: Update, context: CallbackContext):
    welcome_message = (
        "👋 Hello! Welcome to the bot.\n"
        "Here are the available commands:\n"
        "1️⃣ /start -> Show this welcome message\n"
        "2️⃣ /addgroup -> Add the current group to the list of monitored groups\n"
        "3️⃣ /removegroup -> Remove the current group from the list of monitored groups\n"
        "4️⃣ /settargetgroup -> Set the target group for forwarding messages\n"
        "5️⃣ /removetargetgroup -> Remove the target group\n"
        "6️⃣ /joingroup -> Ask the bot to join a new group\n"
        "7️⃣ /enableforwardfromgroups -> Enable forwarding from joined groups\n"
        "8️⃣ /info -> Information about this bot\n"
        "9️⃣ /HowToUse -> Instructions on how to use this bot"
    )
    await update.message.reply_text(welcome_message)


# /HowToUse command to explain how the bot works
async def how_to_use(update: Update, context: CallbackContext):
    instructions = (
        "🛠️ **How to use the bot**:\n"
        "1️⃣ **Add the bot** to a group where you want it to monitor messages.\n"
        "2️⃣ **Use the /addgroup command** from within that group. This command will add the group to the bot’s monitored list.\n"
        "3️⃣ **Set the target group** using the /settargetgroup command. This is the group where the messages will be forwarded.\n"
        "4️⃣ **Remove the target group** using /removetargetgroup command if needed.\n"
        "5️⃣ **The bot will filter and forward** messages from the monitored groups to the target group automatically.\n"
        "6️⃣ **The bot filters out links** and forwards valid messages based on specific patterns."
    )
    await update.message.reply_text(instructions)


# Command to set the target group ID
async def set_target_group(update: Update, context: CallbackContext):
    global TARGET_GROUP_ID
    target_group_id = update.message.chat_id

    if TARGET_GROUP_ID is None:
        TARGET_GROUP_ID = target_group_id
        await update.message.reply_text(f"✅ Target group set to {TARGET_GROUP_ID}.")
    else:
        await update.message.reply_text("⚠️ The target group has already been set.")


# Command to remove the target group ID
async def remove_target_group(update: Update, context: CallbackContext):
    global TARGET_GROUP_ID

    if TARGET_GROUP_ID is not None:
        TARGET_GROUP_ID = None
        await update.message.reply_text("✅ The target group has been removed.")
    else:
        await update.message.reply_text("⚠️ No target group is currently set.")


# Command to add the current group to the list of monitored groups
async def add_group(update: Update, context: CallbackContext):
    group_id = update.message.chat_id
    group_name = update.message.chat.title  # Fetch the group name

    # Prevent adding the target group to the monitored list
    if group_id == TARGET_GROUP_ID:
        await update.message.reply_text("⚠️ You cannot add the target group to the monitored list.")
        return

    if group_id not in source_group_ids:
        if len(source_group_ids) < 5:
            source_group_ids.append(group_id)
            await update.message.reply_text(f"✅ Group '{group_name}' has been added to the monitored list.")
        else:
            await update.message.reply_text("⚠️ You can monitor up to 5 groups only.")
    else:
        await update.message.reply_text(f"⚠️Group '{group_name}' is already being monitored.")


# Command to remove the current group from the monitored list
async def remove_group(update: Update, context: CallbackContext):
    group_id = update.message.chat_id
    group_name = update.message.chat.title

    if group_id in source_group_ids:
        source_group_ids.remove(group_id)
        await update.message.reply_text(f"✅ Group '{group_name}' has been removed from the monitored list.")
    else:
        await update.message.reply_text(f"⚠️ Group '{group_name}' This group is not being monitored.")


# /joingroup command to join a new group using a valid Telegram invite link
async def join_group(update: Update, context: CallbackContext):
    await update.message.reply_text("Please provide the group invite link in the format:\n\n`https://t.me/+<group_code>` 💬")
    
    # This command will expect the user to send the link in the next message
    link = update.message.text

    # Verify the format of the link using regex pattern
    link_pattern = r"^https:\/\/t\.me\/\+\w+$"
    
    if re.match(link_pattern, link):
        try:
            # Use Telegram's API to join the group
            await context.bot.join_chat(link)
            await update.message.reply_text("✅ Successfully joined the group!")
        except Exception as e:
            logger.error(f"Failed to join group: {e}")
            await update.message.reply_text("❌ Error: Could not join the group. Please ensure the link is valid.")
    else:
        await update.message.reply_text("⚠️ Invalid link format! Please provide a valid group invite link like:\n`https://t.me/+<group_code>`")


# /enableforwardfromgroups command to list all joined groups for forwarding
async def enable_forward_from_groups(update: Update, context: CallbackContext):
    if not source_group_ids:
        await update.message.reply_text("🛑 The bot has not joined any groups yet.")
        return
    
    # List groups for user selection
    group_list = "\n".join([f"{i+1}. Group ID: {group_id}" for i, group_id in enumerate(source_group_ids)])
    
    await update.message.reply_text(f"Here are the groups the bot has joined:\n\n{group_list}\n\nPlease select a group by sending its number (e.g., 1). 🟢")


# Filter and forward messages
async def forward_message(update: Update, context: CallbackContext) -> None:
    message = update.message
    logger.info(f"Message received from group {message.chat_id}: {message.text}")

    if message.chat_id in source_group_ids and TARGET_GROUP_ID:
        customized_text = customize_message(message.text or "")
        try:
            await context.bot.send_message(chat_id=TARGET_GROUP_ID, text=customized_text)
            logger.info(f"Message forwarded to target group: {customized_text}")
        except Exception as e:
            logger.error(f"Error forwarding message: {e}")


# Customize the message before forwarding
def customize_message(message_text):
    # Customize the message if needed (currently, no customization)
    return message_text


# Info command to provide information about the bot
async def info(update: Update, context: CallbackContext):
    await update.message.reply_text("For more info, visit: https://www.linkedin.com/in/01neelesh/")


# Main function to run the bot
def main():
    # Create the Application instance
    application = Application.builder().token(API_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("HowToUse", how_to_use))
    application.add_handler(CommandHandler("addgroup", add_group))
    application.add_handler(CommandHandler("removegroup", remove_group))
    application.add_handler(CommandHandler("settargetgroup", set_target_group))
    application.add_handler(CommandHandler("removetargetgroup", remove_target_group))
    application.add_handler(CommandHandler("joingroup", join_group))
    application.add_handler(CommandHandler("enableforwardfromgroups", enable_forward_from_groups))
    application.add_handler(CommandHandler("info", info))

    # Add message handler to forward messages from the source groups
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, forward_message))
    # application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"https://t.me/\+[\w\d]+"), handle_group_link))
    # Run the bot until Ctrl-C is pressed
    application.run_polling()


if __name__ == "__main__":
    main()
