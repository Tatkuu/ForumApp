from flask import Flask, request, redirect, render_template, flash, session, url_for
from os import getenv
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
from models import db
from auth import auth_blueprint
from threads import threads_blueprint
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL', 'postgresql://postgres.gwgcixzhhbqwhqifqbaf:hR84vPLD#M52pj5@aws-0-eu-central-1.pooler.supabase.com:5432/postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = getenv("SECRET_KEY")
db.init_app(app)

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(threads_blueprint, url_prefix='/threads')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)

