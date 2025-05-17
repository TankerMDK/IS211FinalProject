# Blog Application – Final Project (IS211)

This is my final project for the IS211 course. The assignment required students to create a basic Flask web application. I chose to build a **Blog Application**, which allows users to create, view, and manage blog posts using a SQLite database.

---

## Features Implemented (Core Requirements)

- A homepage that displays all published posts in reverse chronological order
- A `/create` route with a form to add new posts
- Each post includes a title, body, slug, creation timestamp, and author
- Individual posts can be viewed via unique URLs
- Posts are stored in a SQLite database
- A working Flask application that runs locally

---

## Extra Credit / Bonus Features

The following features were added as part of the optional extra credit for this project:

- **Edit Post Functionality** – Users can modify the title and body of any post
- **Publish/Unpublish Toggle** – Allows hiding or re-displaying a post without deleting it
- **Permalinks via Slugs** – Posts can be accessed using a slug created from the title
- **Markdown Support** – Posts are rendered using basic Markdown formatting
- **Multi-User Login System** – Users can log in using credentials stored in a database
- **Post Ownership Display** – Each post displays the username of the author
- **Logout Functionality** – Users can log out via a dedicated route

---

## Project Structure

```
project-root/
│
├── app.py              # Main Flask app logic
├── blog.db             # SQLite database
├── README.md           # Project documentation
│
├── templates/          # HTML templates
│   ├── home.html
│   ├── create.html
│   ├── post.html
│   ├── edit.html
│   ├── dashboard.html
│   └── login.html
│
└── static/             # (Optional) CSS or assets — not used in this version
```

---

## How to Run the Project

To run this project locally:

1. Make sure you have Python 3 installed
2. Install required libraries:
   ```
   pip install flask markdown
   ```
3. Start the application:
   ```
   python app.py
   ```
4. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

---

## Login (Extra Credit)

A simple login system was added as an extra credit feature. Credentials are stored in the `users` table in `blog.db`.

Default login options:

| Username       | Password    |
|----------------|-------------|
| `admin`        | `password`  |
| `user1`        | `letmein`   |
| `analyst101`   | `cyber123`  |

Login is required to access the dashboard and post creation/editing routes. Logout is available via `/logout`.

---

## References and Learning Sources

Some features required additional reading outside of the course:

- `markdown` Python library – https://pypi.org/project/Markdown/
- Slug generation logic – implemented manually using a custom slugify() function with re.sub() to create URL-friendly slugs. Inspired by solutions like this Stack Overflow post: https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python
- Flask route examples and query patterns – https://flask.palletsprojects.com/

---

## Notes

The assignment did not require styling or user registration features. However, core features were completed and extra functionality was included to reflect a more real-world blogging experience. All routes include docstrings for clarity, and this README serves to explain the structure and decisions made during development.