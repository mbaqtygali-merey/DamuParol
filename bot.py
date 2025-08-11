import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🔹 Google Sheets API баптау
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "drive.json"  # Service Account JSON файлы
SPREADSHEET_ID = "1YHih90nQMOfh-Z1ak9xbUdwYNA-_IBooODyOaJB-AKQ"  # Мұнда өз ID-ңді жаз

creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1  # ID арқылы ашу

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
TOKEN = os.getenv("BOT_TOKEN")

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find_password))

print("Bot is running...")
app.run_polling()
