import subprocess
from telegram.ext import Updater, CommandHandler

TELEGRAM_TOKEN = "8246638980:AAHaaSeJfBri9UjW5OfC1ivUTCznBbNSUM8"

# Command: /call <number>
def call_command(update, context):
    if len(context.args) != 1:
        update.message.reply_text("Usage: /call <phonenumber>")
        return
    number = context.args[0]
    update.message.reply_text(f"📞 Calling {number}...")

    # Use the already running Asterisk instance via -r
    try:
        subprocess.run(
            ["sudo", "asterisk", "-r", "-x",
             f"channel originate PJSIP/voipms-endpoint/{number} extension 100@from-voipms"],
            check=True
        )
        update.message.reply_text("✅ Call command sent.")
    except subprocess.CalledProcessError as e:
        update.message.reply_text(f"❌ Failed to send call: {e}")

# Command: /results
def results_command(update, context):
    try:
        output = subprocess.check_output(["sudo", "asterisk", "-r", "-x", "core show globals"]).decode()
        last_input = "Not found"
        for line in output.splitlines():
            if "LASTINPUT" in line:
                last_input = line.split()[2]
        update.message.reply_text(f"📋 Last customer input: {last_input}")
    except Exception as e:
        update.message.reply_text(f"Error fetching results: {e}")

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("call", call_command))
    dp.add_handler(CommandHandler("results", results_command))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

