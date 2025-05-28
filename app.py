import os
from flask import Flask, request
import telegram

# Получаем токен и ID группы из переменных окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

if not TOKEN or not GROUP_ID:
    raise ValueError("TELEGRAM_TOKEN и GROUP_ID должны быть заданы в переменных окружения.")

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

# Флаг, чтобы webhook устанавливался один раз
webhook_set = False

@app.route('/')
def home():
    return 'Бот работает!'

@app.route(f'/{TOKEN}', methods=['POST'])
def receive_update():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    if update.message and update.message.photo:
        file_id = update.message.photo[-1].file_id
        bot.send_message(chat_id=GROUP_ID, text="Получено фото от пользователя")
        bot.send_photo(chat_id=GROUP_ID, photo=file_id)
    return 'ok'

@app.after_request
def set_webhook_once(response):
    global webhook_set
    if not webhook_set:
        webhook_url = f"https://tg-server-bot.onrender.com/{TOKEN}"
        bot.set_webhook(url=webhook_url)
        webhook_set = True
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
