import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import json
from google.oauth2.service_account import Credentials

# 🔹 Google Sheets API баптау
creds_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(creds_info, scopes=scope)
client = gspread.authorize(creds)

# Мұнда Google Sheets-тің ID және бет атауын жазыңыз
SHEET_ID = "1YHih90nQMOfh-Z1ak9xbUdwYNA-_IBooODyOaJB-AKQ"
sheet = client.open_by_key(SHEET_ID).sheet1

# 🔹 /start командасы
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Сәлем! Мен Lira сайтының ИИ көмекшісімін. Маған ЖСН-іңізді жазыңыз, мен парольді табамын.")

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
        await update.message.reply_text(f"Сіздің пароліңіз: 
        {password}")
    else:
        await update.message.reply_text("Бұл ЖСН бойынша пароль табылмады немесе басқа үйірмеге тіркелгенсіз.")

# 🔹 Telegram ботты іске қосу
TOKEN = os.getenv("BOT_TOKEN")  # Render-да BOT_TOKEN орта айнымалысына мән беріңіз

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find_password))

print("Bot is running...")
app.run_polling()
