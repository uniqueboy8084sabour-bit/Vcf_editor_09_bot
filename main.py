import os
import threading
import telebot
from flask import Flask

# Fetch tokens from environment variables
BOT_TOKEN = os.environ.get("bot_token")
HF_TOKEN = os.environ.get("hf_token")

# Initialize the Telegram bot and Flask app
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Start command
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Hello! 🤖 Bot is working!")

# Echo message
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.text != "/start":
        bot.send_message(message.chat.id, "You said: " + message.text)

# Dummy web server route to satisfy Render's port binding requirement
@app.route('/')
def home():
    return "Bot is running smoothly!"

# Function to run the bot polling
def run_bot():
    print("Bot is running...")
    bot.infinity_polling()

if __name__ == "__main__":
    # Start the Telegram bot in a separate background thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    # Start the Flask web server in the main thread
    # Render automatically provides a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
