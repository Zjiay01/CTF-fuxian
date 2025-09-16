from flask import Flask, request, render_template, redirect, url_for, flash, render_template_string, make_response
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import requests
from markupsafe import escape
from playwright.sync_api import sync_playwright
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password, bio=""):
        self.id = id
        self.username = username
        self.password = password
        self.bio = bio
admin_password = os.urandom(12).hex()

USERS_DB = {'admin': User(id=1, username='admin', password=admin_password)}
USER_ID_COUNTER = 1

@login_manager.user_loader
def load_user(user_id):
    for user in USERS_DB.values():
        if str(user.id) == user_id:
            return user
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    global USER_ID_COUNTER
    if request.method == 'POST':
        username = request.form['username']
        if username in USERS_DB:
            flash('Username already exists.')
            return redirect(url_for('register'))
        
        USER_ID_COUNTER += 1
        new_user = User(
            id=USER_ID_COUNTER,
            username=username,
            password=request.form['password']
        )
        USERS_DB[username] = new_user
        login_user(new_user)
        response = make_response(redirect(url_for('index')))
        response.set_cookie('ticket', 'your_ticket_value')
        return response
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = USERS_DB.get(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.bio = request.form['bio']
        print(current_user.bio)
        return redirect(url_for('index'))
    return render_template('profile.html')

@app.route('/ticket', methods=['GET', 'POST'])
def ticket():
    if request.method == 'POST':
        ticket = request.form['ticket']
        response = make_response(redirect(url_for('index')))
        response.set_cookie('ticket', ticket)
        return response
    return render_template('ticket.html')

@app.route("/view", methods=["GET"])
@login_required
def view_user():
    """
    # I found a bug in it.
    # Until I fix it, I've banned /api/bio/. Have fun :)
    """
    username = request.args.get("username",default=current_user.username)
    visit_url(f"http://localhost/api/bio/{username}")
    template = f"""
    {{% extends "base.html" %}}
    {{% block title %}}success{{% endblock %}}
    {{% block content %}}
    <h1>bot will visit your bio</h1>
    <p style="margin-top: 1.5rem;"><a href="{{{{ url_for('index') }}}}">Back to Home</a></p>
    {{% endblock %}}
    """
    return render_template_string(template)


@app.route("/api/bio/<string:username>", methods=["GET"])
@login_required
def get_user_bio(username):
    if not current_user.username == username:
        return "Unauthorized", 401
    user = USERS_DB.get(username)
    if not user:
        return "User not found.", 404
    return user.bio

def visit_url(url):
    try:
        flag_value = os.environ.get('FLAG', 'flag{fake}')

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            context = browser.new_context()

            context.add_cookies([{
                'name': 'flag',
                'value': flag_value,
                'domain': 'localhost',
                'path': '/',
                'httponly': True
            }])

            page = context.new_page()
            page.goto("http://localhost/login", timeout=5000)
            page.fill("input[name='username']", "admin")
            page.fill("input[name='password']", admin_password)
            page.click("input[name='submit']")
            page.wait_for_timeout(3000)
            page.goto(url, timeout=5000)
            page.wait_for_timeout(5000)
            browser.close()

    except Exception as e:
        print(f"Bot error: {str(e)}")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)