from flask import Flask, request, redirect, render_template, flash, session, url_for
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from models import Thread, Comment, User, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres'
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
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Tallenna käyttäjän id sessioniin
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
        user_exists = User.query.filter_by(username=username).first()

        if user_exists:
            flash('Username already exists')
            return redirect(url_for("register"))

        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash('User successfully registered')
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
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

        new_thread = Thread(title=title, user_id=user_id)
        db.session.add(new_thread)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_thread.html')

@app.route('/threads/<int:thread_id>')
def show_thread(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    comments = Comment.query.filter_by(thread_id=thread.id).all()
    return render_template('thread.html', thread=thread, comments=comments)


@app.route('/threads')
def threads():
    all_threads = Thread.query.all()
    return render_template('threads.html', threads=all_threads)


@app.route('/threads/<int:thread_id>/comment', methods=['POST'])
def comment(thread_id):
    if 'user_id' not in session:
        flash('Please log in to comment.')
        return redirect(url_for('login'))
    content = request.form.get('content')
    new_comment = Comment(content=content, thread_id=thread_id, user_id=session['user_id'])
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('show_thread', thread_id=thread_id))


#Vanha kommentointi
'''@app.route('/threads/<int:thread_id>/comment', methods=['POST'])
def comment(thread_id):
    if 'user_id' not in session:
        flash('Please log in to comment.')
        return redirect(url_for('login'))

    content = request.form.get('content')
    user_id = session.get('user_id')

    if not content:
        flash('Content is required.')
        return redirect(url_for('thread', thread_id=thread_id))

    comment = Comment(content=content, thread_id=thread_id, user_id=user_id)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('threads'))'''

@app.route('/comments/<int:comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != session.get('user_id'):
        flash('You do not have permission to delete this comment.')
        return redirect(url_for('index'))

    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('threads'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

