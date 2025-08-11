import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🔹 Google Sheets API баптау
import os
import json
import gspread
from google.oauth2.service_account import Credentials

creds_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(creds_info, scopes=scope)
client = gspread.authorize(creds)


# 🔹 /start командасы
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Сәлем! Маған ЖСН-іңізді жазыңыз, мен парольді табамын.")

# 🔹 ЖСН енгізген кезде
async def find_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jsn = update.message.text.strip()
    
    if not jsn.isdigit():
        await update.message.reply_text("ЖСН тек цифрдан тұруы керек!")
        return

    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    result = df[df['JSN'].astype(str) == jsn]
    if not result.empty:
        password = result.iloc[0]['Password']
        await update.message.reply_text(f"Сіздің пароліңіз: {password}")
    else:
        await update.message.reply_text("Бұл ЖСН бойынша пароль табылмады.")

# 🔹 Telegram ботты іске қосу
import os
TOKEN = os.getenv("8202497661:AAGfIb6MS9nzg4IyDs6gSm_PqXqUzB7e0wg")

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find_password))

print("Bot is running...")
app.run_polling()
