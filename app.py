from flask import Flask, render_template, request, redirect, url_for, abort, session
import sqlite3
from datetime import datetime
import os
import re
import markdown

app = Flask(__name__)
app.secret_key = 'a_super_secret_key'

DATABASE = 'blog.db'

# I hope this works
def get_db_connection():
    """Opens a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the database with the posts table if it doesn't exist."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            published INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()


def init_users_table():
    """Creates a basic users table and seeds multiple default users."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    default_users = [
        ('admin', 'password'),
        ('user1', 'letmein'),
        ('analyst101', 'cyber123')
    ]

    for username, password in default_users:
        conn.execute(
            "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

    conn.commit()
    conn.close()


@app.route("/")
def index():
    """
    Homepage route. Displays all published blog posts with their author's username.
    """
    conn = get_db_connection()
    posts = conn.execute('''
        SELECT posts.*, users.username
        FROM posts
        JOIN users ON posts.user_id = users.id
        WHERE posts.published = 1
        ORDER BY posts.created_at DESC
    ''').fetchall()
    conn.close()
    return render_template("home.html", posts=posts)


def slugify(title):
    """Converts a blog post title into a URL-friendly slug."""
    slug = re.sub(r'\W+', '-', title.lower()).strip('-')
    return slug


@app.route("/create", methods=["GET", "POST"])
def create():
    """
    Displays a form to create a new post.
    On submission, saves the post with current timestamp and generated slug.
    """
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        slug = slugify(title)
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        user_id = session.get("user_id")

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO posts (title, body, slug, published, created_at, user_id) VALUES (?, ?, ?, ?, ?, ?)",
            (title, body, slug, 1, created_at, user_id)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("create.html")



@app.route("/post/<slug>")
def post(slug):
    """
    Fetches a single post by slug, including author's username, and displays it.
    """
    conn = get_db_connection()
    post = conn.execute('''
        SELECT posts.*, users.username
        FROM posts
        JOIN users ON posts.user_id = users.id
        WHERE posts.slug = ?
    ''', (slug,)).fetchone()
    conn.close()

    if post is None:
        abort(404)

    body_html = markdown.markdown(post["body"])

    return render_template("post.html", post=post, body_html=body_html)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    """
    Allows a user to edit an existing blog post.
    GET: Pre-fills form with post data.
    POST: Saves updated title, body, and slug.
    """
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (id,)).fetchone()

    if post is None:
        conn.close()
        abort(404)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        slug = slugify(title)

        conn.execute(
            "UPDATE posts SET title = ?, body = ?, slug = ? WHERE id = ?",
            (title, body, slug, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("post", slug=slug))

    conn.close()
    return render_template("edit.html", post=post)


@app.route("/toggle/<int:id>")
def toggle_publish(id):
    """
    Flips the 'published' status of a blog post.
    If published → unpublishes it.
    If unpublished → republishes it.
    """
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (id,)).fetchone()

    if post is None:
        conn.close()
        abort(404)

    new_status = 0 if post["published"] else 1

    conn.execute(
        "UPDATE posts SET published = ? WHERE id = ?",
        (new_status, id)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/dashboard")
def dashboard():
    """
    Shows a management view of all blog posts, regardless of publish status.
    Includes links to edit, toggle visibility, and create new posts.
    """
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("dashboard.html", posts=posts)


@app.route("/delete/<int:id>")
def delete(id):
    """
    Deletes a blog post by ID.
    Redirects back to the dashboard after deletion.
    """
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Displays a login form and verifies user credentials from the users table.
    On success, sets session and redirects to dashboard.
    """
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid credentials"

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    """
    Logs the user out by clearing the session and redirecting to the homepage.
    """
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        init_db()
        init_users_table()
    app.run(debug=True)
