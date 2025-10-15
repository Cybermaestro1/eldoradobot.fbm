# import os
import requests
import pandas as pd
import yfinance as yf
import ta
import telebot
from telebot import types
import logging
import random
from datetime import datetime, timezone
from flask import Flask, request
import threading
import json
from dotenv import load_dotenv

# ---------------- LOAD ENV VARIABLES ----------------
load_dotenv()  # loads .env file in local testing
BOT_TOKEN = os.getenv("BOT_TOKEN")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NOWPAYMENTS_API_KEY = os.getenv("NOWPAYMENTS_API_KEY")
VIP_FILE = "vip_users.json"

bot = telebot.TeleBot(BOT_TOKEN)
user_timeframes = {}

# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ---------------- VIP PERSISTENCE ----------------
if os.path.exists(VIP_FILE):
    with open(VIP_FILE, "r") as f:
        vip_users = set(json.load(f))
else:
    vip_users = set()

def save_vip_users():
    with open(VIP_FILE, "w") as f:
        json.dump(list(vip_users), f)

# ---------------- HELP FUNCTION ----------------
MAX_MESSAGE_LENGTH = 4000
def send_long_message(chat_id, text, markup=None):
    for i in range(0, len(text), MAX_MESSAGE_LENGTH):
        bot.send_message(chat_id, text[i:i+MAX_MESSAGE_LENGTH], reply_markup=markup if i == 0 else None)

# ---------------- NEWS ----------------
def fetch_news(query=None, page_size=7):
    if not NEWS_API_KEY:
        return "⚠️ News API key not configured."
    base = "https://newsapi.org/v2/everything"
    if not query:
        query = (
            "gold OR GC=F OR bitcoin OR btc OR ethereum OR eth OR crypto OR "
            "forex OR currency OR usd OR eur OR gbp OR jpy OR fx OR "
            "s&p OR spx OR nasdaq OR dow OR stocks OR equities"
        )
    params = {"q": query,"language":"en","pageSize":page_size,"sortBy":"publishedAt","apiKey":NEWS_API_KEY}
    try:
        resp = requests.get(base, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "ok":
            return "⚠️ Failed to fetch news."
        articles = data.get("articles", [])
        if not articles:
            return "ℹ️ No recent market headlines found."
        lines = ["📰 Top Market News:\n"]
        for i, a in enumerate(articles, 1):
            title = a.get("title", "No title")
            source = a.get("source", {}).get("name", "Unknown")
            url = a.get("url", "")
            published = a.get("publishedAt")
            try:
                ts = datetime.fromisoformat(published.replace("Z", "+00:00")).astimezone(timezone.utc)
                published_str = ts.strftime("%Y-%m-%d %H:%M UTC")
            except:
                published_str = published or ""
            lines.append(f"{i}. {title} — {source} ({published_str})\n{url}\n")
        lines.append("\n🔎 Use /news <keyword> to search specific topics.")
        lines.append("\n🔗 Powered by Eldorado.FBM Bot")
        return "\n".join(lines)
    except Exception as e:
        logger.exception("News fetch error")
        return "⚠️ Error fetching news."

# ---------------- GOLD REPORT ----------------
def build_gold_report(interval="1d", period="6mo", quick=False):
    # (copy your existing gold report code here)
    pass  # Keep your existing code; replace hardcoded keys with variables

# ---------------- NOWPAYMENTS ----------------
def generate_nowpayments_invoice(user_id, amount_usd=5):
    url = "https://api.nowpayments.io/v1/invoice"
    headers = {"x-api-key": NOWPAYMENTS_API_KEY, "Content-Type": "application/json"}
    data = {
        "price_amount": amount_usd,
        "price_currency": "usd",
        "pay_currency": "usd,btc,eth,usdt",
        "order_id": str(user_id),
        "ipn_callback_url": "https://YOUR_RENDER_SERVICE_URL/nowpayments-ipn"
    }
    try:
        resp = requests.post(url, json=data, headers=headers, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        return result.get("invoice_url")
    except Exception as e:
        logger.exception("NowPayments invoice error")
        return None

# ---------------- BOT HANDLERS ----------------
# Copy your bot handlers and callbacks here from your code, replacing keys with environment variables

# ---------------- FLASK APP ----------------
app = Flask(__name__)

@app.route("/nowpayments-ipn", methods=["POST"])
def nowpayments_ipn():
    data = request.json
    if not data:
        return "No data", 400
    order_id = data.get("order_id")
    payment_status = data.get("payment_status")
    if order_id and payment_status in ["finished","confirmed"]:
        user_id = int(order_id)
        vip_users.add(user_id)
        save_vip_users()
        try:
            bot.send_message(user_id, "🎉 Your VIP Upgrade is confirmed! Enjoy premium features.")
        except:
            pass
    return "OK", 200

# ---------------- RUN BOT & FLASK ----------------
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

def run_bot():
    bot.infinity_polling(timeout=60, long_polling_timeout=60)

threading.Thread(target=run_flask).start()
threading.Thread(target=run_bot).start()
Paste your existing app.py code here (the full code you provided)
# Ensure this is the same code you want to deploy
