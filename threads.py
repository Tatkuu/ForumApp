from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from sqlalchemy import text
from models import db

threads_blueprint = Blueprint('threads', __name__, template_folder='templates')

@threads_blueprint.route('/new', methods=['GET', 'POST'])
def new_thread():
    if 'user_id' not in session:
        flash('Please log in to start a new thread.')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        user_id = session.get('user_id')

        if not title:
            flash('Title is required.')
            return redirect(url_for('threads.new_thread'))

        sql = text("INSERT INTO threads (title, user_id) VALUES (:title, :user_id)")
        db.session.execute(sql, {"title": title, "user_id": user_id})
        db.session.commit()
        return redirect(url_for('threads.threads'))
    return render_template('new_thread.html')

@threads_blueprint.route('/')
def threads():
    sql = text("""
        SELECT threads.id, threads.title, users.username, threads.created_at 
        FROM threads 
        JOIN users ON threads.user_id = users.id
    """)
    all_threads = db.session.execute(sql).fetchall()
    return render_template('threads.html', threads=all_threads)


@threads_blueprint.route('/<int:thread_id>')
def show_thread(thread_id):
    try:
        thread_sql = text("SELECT id, title, user_id, created_at FROM threads WHERE id = :thread_id")
        thread_result = db.session.execute(thread_sql, {"thread_id": thread_id}).fetchone()
        
        if not thread_result:
            flash('Thread not found')
            return redirect(url_for('threads.threads'))

        comments_sql = text("SELECT id, content, user_id, created_at FROM comments WHERE thread_id = :thread_id ORDER BY created_at")
        comments_result = db.session.execute(comments_sql, {"thread_id": thread_id}).fetchall()

        return render_template('thread.html', thread=thread_result, comments=comments_result)
    except Exception as e:
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('threads.threads'))



@threads_blueprint.route('/<int:thread_id>/comment', methods=['POST'])
def comment(thread_id):
    if 'user_id' not in session:
        flash('Please log in to comment.')
        return redirect(url_for('auth.login'))
    
    content = request.form.get('content')
    user_id = session.get('user_id')
    if content:
        try:
            sql = text("INSERT INTO comments (content, thread_id, user_id) VALUES (:content, :thread_id, :user_id)")
            db.session.execute(sql, {"content": content, "thread_id": thread_id, "user_id": user_id})
            db.session.commit()
            flash('Comment added successfully.')
        except Exception as e:
            flash(f'Error adding comment: {str(e)}')
    else:
        flash('Comment cannot be empty.')

    return redirect(url_for('threads.show_thread', thread_id=thread_id))


@threads_blueprint.route('/comments/<int:comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    if 'user_id' not in session:
        flash('Please log in to delete comments.')
        return redirect(url_for('auth.login'))

    comment_sql = text("SELECT user_id, thread_id FROM comments WHERE id = :comment_id")
    result = db.session.execute(comment_sql, {"comment_id": comment_id})
    comment = result.first()

    if comment and comment[0] == session.get('user_id'):
        delete_sql = text("DELETE FROM comments WHERE id = :comment_id")
        db.session.execute(delete_sql, {"comment_id": comment_id})
        db.session.commit()
        flash('Comment deleted successfully.')
        return redirect(url_for('threads.show_thread', thread_id=comment[1]))
    else:
        flash('You do not have permission to delete this comment.')
        return redirect(url_for('threads.threads'))





@threads_blueprint.route('/<int:thread_id>/delete', methods=['POST'])
def delete_thread(thread_id):
    if 'user_id' not in session:
        flash('Please log in to delete threads.')
        return redirect(url_for('auth.login'))

    thread_sql = text("SELECT user_id FROM threads WHERE id = :thread_id")
    result = db.session.execute(thread_sql, {"thread_id": thread_id})
    thread = result.first()

    if thread and thread[0] == session.get('user_id'):
        delete_comments_sql = text("DELETE FROM comments WHERE thread_id = :thread_id")
        db.session.execute(delete_comments_sql, {"thread_id": thread_id})

        delete_thread_sql = text("DELETE FROM threads WHERE id = :thread_id")
        db.session.execute(delete_thread_sql, {"thread_id": thread_id})
        db.session.commit()
        flash('Thread deleted successfully.')
        return redirect(url_for('threads.threads'))
    else:
        flash('You do not have permission to delete this thread.')
        return redirect(url_for('threads.threads'))

@threads_blueprint.route('/search')
def search():
    search_term = request.args.get('query', '')
    search_term = f"%{search_term}%"
    sql = text("""
        SELECT threads.id, threads.title, users.username, threads.created_at 
        FROM threads
        JOIN users ON threads.user_id = users.id
        WHERE threads.title ILIKE :search
        ORDER BY threads.created_at DESC;
    """)
    threads = db.session.execute(sql, {'search': search_term}).fetchall()
    return render_template('search_results.html', threads=threads)

