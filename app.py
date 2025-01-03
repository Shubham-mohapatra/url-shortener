import random
import string
import sqlite3
from flask import Flask, redirect, request, render_template, url_for

from create_db import create_database

app = Flask(__name__)
DB_NAME = 'url_shortener.db'

# Generate a short URL
def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# Insert short URL and original URL into the database
def insert_url(short_url, long_url):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO urls (short_url, long_url) VALUES (?, ?)", (short_url, long_url))

# Retrieve the original URL for a given short URL
def get_long_url(short_url):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.execute("SELECT long_url FROM urls WHERE short_url = ?", (short_url,))
        row = cur.fetchone()
        return row[0] if row else None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return "URL is required", 400

        # Generate a short URL
        short_url = generate_short_url()
        while get_long_url(short_url):  # Ensure the short URL is unique
            short_url = generate_short_url()

        # Store the short URL in the database
        insert_url(short_url, url)

        # Redirect the user directly to the original website
        return redirect(url)

    # Display the HTML form to the user
    return render_template("index.html")

@app.route('/<short_url>')
def redirect_to_original(short_url):
    url = get_long_url(short_url)
    if url:
        return redirect(url)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
