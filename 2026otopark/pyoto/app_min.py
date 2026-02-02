from flask import Flask

app = Flask(__name__)

from flask_login import LoginManager

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader

def load_user(user_id):

    return None

@app.route('/')
def index():
    return 'Hello'

if __name__ == '__main__':
    app.run()