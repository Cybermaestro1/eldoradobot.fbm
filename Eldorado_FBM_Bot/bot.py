import telebot
import pandas as pd
import yfinance as yf
import requests

# ---------------- CONFIG ----------------
BOT_TOKEN = "8403553868:AAFEXgwFvPR2SR70Eb5OxqfLmu6edALEG2k"
NEWS_API_KEY = "cd54dad334e440809fe05a52f6f26db3"
NOWPAYMENTS_API_KEY = "FABZQWK-ZFSMAFR-KK975K3-TJPC8BY"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! Eldorado.FBM Bot is running.")

@bot.message_handler(commands=['gold'])
def gold_price(message):
    data = yf.download("GC=F", period="1d", interval="1h")
    last_close = data['Close'].iloc[-1]
    bot.reply_to(message, f"Latest Gold Price: ${last_close:.2f}")

if __name__ == "__main__":
    bot.polling()