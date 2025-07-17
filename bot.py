import os
import requests
import datetime
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Load environment variables from .env file
load_dotenv()

# Load secrets from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_SHEET_NAME = 'Apollo Bot Logs'
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_PATH, scope)
client = gspread.authorize(creds)
sheet = client.open(GOOGLE_SHEET_NAME).sheet1

# Mock Apollo search function
def search_apollo(name):
    fake_people = {
        "Elon Musk": {
            "name": "Elon Musk",
            "title": "CEO",
            "organization_name": "SpaceX",
            "email": "elon@spacex.com",
            "linkedin_url": "https://linkedin.com/in/elonmusk"
        },
        "Sundar Pichai": {
            "name": "Sundar Pichai",
            "title": "CEO",
            "organization_name": "Google",
            "email": "sundar@google.com",
            "linkedin_url": "https://linkedin.com/in/sundarpichai"
        },
        "Satya Nadella": {
            "name": "Satya Nadella",
            "title": "CEO",
            "organization_name": "Microsoft",
            "email": "satya@microsoft.com",
            "linkedin_url": "https://linkedin.com/in/satyanadella"
        }
    }

    person = fake_people.get(name.strip(), None)
    if not person:
        return f"No data found for '{name}'. Try: Elon Musk, Sundar Pichai, or Satya Nadella."

    return f"""{person['name']} - {person['title']} at {person['organization_name']}
Email: {person['email']}
LinkedIn: {person['linkedin_url']}"""

# Log to Google Sheet
def log(prompt, result):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([time, prompt, result])

# Telegram message handler
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    result = search_apollo(prompt)
    log(prompt, result)
    await update.message.reply_text(result)

# Main bot logic
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle))
    print("✅ Bot is running. Type a name in Telegram.")
    app.run_polling()

if __name__ == '__main__':
    main()
