import os
import base64
from io import BytesIO
from flask import Flask, request, render_template, jsonify
import telegram

# Получение токена и ID группы из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

if not TOKEN or not GROUP_ID:
    raise ValueError("BOT_TOKEN and GROUP_ID must be set in environment variables.")

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_to_telegram():
    caption = request.form.get("caption", "No message")
    photo_base64 = request.form.get("photoBase64")

    # Если фото отсутствует — отправляем только текст
    if not photo_base64:
        try:
            bot.send_message(chat_id=GROUP_ID, text=caption)
        except Exception as e:
            return jsonify({"error": f"Error sending message to Telegram: {str(e)}"}), 500
        return jsonify({"success": True}), 200

    # Удаляем префикс base64
    if photo_base64.startswith("data:image"):
        photo_base64 = photo_base64.split(",", 1)[1]

    try:
        image_data = base64.b64decode(photo_base64)
    except Exception as e:
        return jsonify({"error": f"Error decoding image: {str(e)}"}), 400

    image_file = BytesIO(image_data)
    image_file.name = "photo.jpg"

    try:
        bot.send_photo(chat_id=GROUP_ID, photo=image_file, caption=caption)
    except Exception as e:
        return jsonify({"error": f"Error sending to Telegram: {str(e)}"}), 500

    return jsonify({"success": True}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
