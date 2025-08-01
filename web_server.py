from flask import Flask
import asyncio
import os
import threading
from telegram_bot import main as start_bot

app = Flask(__name__)

@app.route('/')
def index():
    return "🤖 Telegram-бот УрФУ работает!"

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot())

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
