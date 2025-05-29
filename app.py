import os
from flask import Flask, request, render_template
import telegram
from io import BytesIO

# Получаем токен и ID группы из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

if not TOKEN or not GROUP_ID:
    raise ValueError("BOT_TOKEN и GROUP_ID должны быть заданы в переменных окружения.")

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_photo', methods=['POST'])
def send_photo():
    photo = request.files.get('photo')
    if not photo:
        return 'No photo uploaded', 400

    # Преобразуем в формат, понятный Telegram API
    byte_io = BytesIO()
    photo.save(byte_io)
    byte_io.seek(0)

    bot.send_message(chat_id=GROUP_ID, text="Получено фото с сайта")
    bot.send_photo(chat_id=GROUP_ID, photo=byte_io)

    return 'ok', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
