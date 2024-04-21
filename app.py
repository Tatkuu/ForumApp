from flask import Flask, request, redirect, render_template, flash, session, url_for
from os import getenv
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
from models import db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL', 'postgresql://postgres.gwgcixzhhbqwhqifqbaf:hR84vPLD#M52pj5@aws-0-eu-central-1.pooler.supabase.com:5432/postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = getenv("SECRET_KEY")
db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sql = text("SELECT * FROM users WHERE username = :username")
        result = db.session.execute(sql, {"username": username})
        user = result.fetchone()
        if user and check_password_hash(user.password, password):  # Changed indexing method
            session['user_id'] = user.id  # Changed indexing method
            flash('You were successfully logged in')
            return redirect(url_for("index"))
        else:
            flash('Invalid username or password')
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sql = text("SELECT username FROM users WHERE username = :username")
        result = db.session.execute(sql, {"username": username})
        user_exists = result.fetchone()
        if user_exists:
            flash('Username already exists')
            return redirect(url_for("register"))

        hash_password = generate_password_hash(password)
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username": username, "password": hash_password})
        db.session.commit()
        flash('User successfully registered')
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/threads/new', methods=['GET', 'POST'])
def new_thread():
    if 'user_id' not in session:
        flash('Please log in to start a new thread.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        user_id = session.get('user_id')

        if not title:
            flash('Title is required.')
            return redirect(url_for('new_thread'))

        sql = text("INSERT INTO threads (title, user_id) VALUES (:title, :user_id)")
        db.session.execute(sql, {"title": title, "user_id": user_id})
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_thread.html')

@app.route('/threads/<int:thread_id>')
def show_thread(thread_id):
    sql = text("SELECT * FROM threads WHERE id = :thread_id")
    result = db.session.execute(sql, {"thread_id": thread_id})
    thread = result.fetchone()
    if thread:
        sql_comments = text("SELECT * FROM comments WHERE thread_id = :thread_id")
        comments = db.session.execute(sql_comments, {"thread_id": thread_id}).fetchall()
        return render_template('thread.html', thread=thread, comments=comments)
    else:
        flash('Thread not found')
        return redirect(url_for('index'))

@app.route('/threads')
def threads():
    sql = text("""
        SELECT threads.id, threads.title, users.username, threads.created_at 
        FROM threads 
        JOIN users ON threads.user_id = users.id
    """)
    all_threads = db.session.execute(sql).fetchall()
    return render_template('threads.html', threads=all_threads)


@app.route('/threads/<int:thread_id>/comment', methods=['POST'])
def comment(thread_id):
    if 'user_id' not in session:
        flash('Please log in to comment.')
        return redirect(url_for('login'))
    
    content = request.form.get('content')
    user_id = session.get('user_id')
    sql = text("INSERT INTO comments (content, thread_id, user_id) VALUES (:content, :thread_id, :user_id)")
    db.session.execute(sql, {"content": content, "thread_id": thread_id, "user_id": user_id})
    db.session.commit()
    return redirect(url_for('show_thread', thread_id=thread_id))

@app.route('/comments/<int:comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    sql_check_user = text("SELECT user_id FROM comments WHERE id = :comment_id")
    result = db.session.execute(sql_check_user, {"comment_id": comment_id})
    comment = result.fetchone()
    if comment and comment['user_id'] == session.get('user_id'):
        sql_delete = text("DELETE FROM comments WHERE id = :comment_id")
        db.session.execute(sql_delete, {"comment_id": comment_id})
        db.session.commit()
        flash('Comment deleted')
    else:
        flash('You do not have permission to delete this comment.')
    return redirect(url_for('threads'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


