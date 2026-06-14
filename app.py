import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests

# Pydroid የፎልደሩን መንገድ በትክክል እንዲያገኝ መከላከያ
template_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(template_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'super_secure_key_for_friends_app'

# ⚠️ PLACE YOUR TELEGRAM DETAILS HERE
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
MY_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID_HERE"

# Pre-registered friends database
ALLOWED_FRIENDS = {
    "Asefa Kebede": {"email": "asefa@gmail.com", "password": "asefaPassword123"},
    "Fozia Ahmed": {"email": "fozia@gmail.com", "password": "foziaSecurePass"},
    "Henok Tadese": {"email": "henok@gmail.com", "password": "henokPassword3"}
}

# Temporary storage to track login approvals
PENDING_REQUESTS = {}

def send_telegram_notification(username):
    text = f"🚨 *Login Request!*\n\nFriend: 👤 *{username}* is trying to access the website.\n\n👉 *To ALLOW click here:*\nhttp://127.0.0.1:5000/approve/{username}\n\n👉 *To DENY click here:*\nhttp://127.0.0.1:5000/reject/{username}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": MY_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try: requests.post(url, json=payload)
    except Exception as e: print(f"Error: {e}")

@app.route('/')
def home():
    if 'logged_in' in session:
        return f"<h1>Welcome, {session['user']}! 🎉 This is our 3-Year Anniversary Page!</h1><br><a href='/logout'>Logout</a>"
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()
        
        if username in ALLOWED_FRIENDS and ALLOWED_FRIENDS[username]['email'] == email and ALLOWED_FRIENDS[username]['password'] == password:
            PENDING_REQUESTS[username] = "waiting"
            send_telegram_notification(username)
            return render_template('login.html', waiting_for=username)
        
        return "<h3>Security Error: Invalid Details!</h3><a href='/login'>Try Again</a>"
            
    return render_template('login.html', waiting_for=None)

@app.route('/approve/<username>')
def approve(username):
    if username in PENDING_REQUESTS:
        PENDING_REQUESTS[username] = "approved"
        return f"Access ALLOWED for {username}! ✅"
    return "Request not found."

@app.route('/reject/<username>')
def reject(username):
    if username in PENDING_REQUESTS:
        PENDING_REQUESTS[username] = "rejected"
        return f"Access DENIED for {username}! ❌"
    return "Request not found."

@app.route('/check_status/<username>')
def check_status(username):
    status = PENDING_REQUESTS.get(username, "none")
    return jsonify({"status": status})

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
