import os
from flask import Flask, request, render_template
import telegram

TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

if not TOKEN or not GROUP_ID:
    raise ValueError("BOT_TOKEN и GROUP_ID должны быть заданы в переменных окружения.")

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_photo():
    photo = request.files['photo']
    if photo:
        bot.send_message(chat_id=GROUP_ID, text="Фото с сайта:")
        bot.send_photo(chat_id=GROUP_ID, photo=photo)
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
