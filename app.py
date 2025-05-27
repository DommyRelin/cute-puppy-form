import os
from flask import Flask, request
import telegram

# Получаем токен и ID группы из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

# Проверка: если переменные не заданы
if not TOKEN or not GROUP_ID:
    raise ValueError("BOT_TOKEN и GROUP_ID должны быть заданы в переменных окружения.")

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return 'Бот работает!'

@app.route(f'/{TOKEN}', methods=['POST'])
def receive_update():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    if update.message:
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
            bot.send_message(chat_id=GROUP_ID, text="Получено фото от пользователя")
            bot.send_photo(chat_id=GROUP_ID, photo=file_id)
    return 'ok'

if __name__ == '__main__':
    app.run(port=5000)
