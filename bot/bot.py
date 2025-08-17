import asyncio
import logging
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Telegram bot token
TELEGRAM_TOKEN = "8246638980:AAHaaSeJfBri9UjW5OfC1ivUTCznBbNSUM8"

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# --- Command Handlers ---

async def call_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /call <phonenumber>")
        return

    number = context.args[0]
    await update.message.reply_text(f"📞 Calling {number}...")
    
    try:
        subprocess.run([
            "asterisk", "-rx",
            f"channel originate PJSIP/voipms-endpoint/{number} extension 100@from-voipms"
        ], check=True)
        logging.info(f"Call attempted to {number}")
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"Error calling {number}: {e}")
        logging.error(f"Error calling {number}: {e}")

async def results_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        output = subprocess.check_output(
            ["asterisk", "-rx", "core show globals"]
        ).decode()
        last_input = "Not found"
        for line in output.splitlines():
            if "LASTINPUT" in line:
                last_input = line.split()[2]
        await update.message.reply_text(f"📋 Last customer input: {last_input}")
    except Exception as e:
        await update.message.reply_text(f"Error fetching results: {e}")
        logging.error(f"Error fetching results: {e}")

# --- Main bot setup ---
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("call", call_command))
    app.add_handler(CommandHandler("results", results_command))

    logging.info("Clearing pending updates...")
    updates = await app.bot.get_updates(offset=-1)
    logging.info(f"Cleared {len(updates)} pending updates")

    logging.info("Bot is starting polling...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # Keep bot alive indefinitely
    await asyncio.Event().wait()

# --- Entry point ---
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:  # if a loop is already running (Cloud Shell / Jupyter)
        loop = asyncio.get_running_loop()
        loop.create_task(main())
