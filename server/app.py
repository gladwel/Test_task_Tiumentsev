from flask import Flask, render_template_string
from psycopg2 import connect
import json

app = Flask(__name__)

db_conn = connect(
    host='db',
    port=5432,
    dbname='sreality',
    user='sreality_user',
    password='sreality_password'
)

@app.route('/')
def index():
    with db_conn:
        with db_conn.cursor() as cur:
            cur.execute("SELECT title, image_url FROM ads")
            ads = cur.fetchall()
            #delete all non-ascii characters in title
            ads = [(title.encode('ascii', 'ignore').decode('ascii'), image_url) for title, image_url in ads]

    return render_template_string('''
        <!DOCTYPE html>
<html>
<head>
    <title>Scraped Ads</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        h1 {
            text-align: center;
            padding: 20px;
            background-color: #f2f2f2;
        }
        ul {
            list-style-type: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
        }
        li {
            margin: 10px;
            padding: 10px;
            width: 300px;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
        }
        h2 {
            margin: 0;
            padding: 0;
        }
        img {
            max-width: 100%;
            height: auto;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h1>Scraped Ads</h1>
    <ul>
        {% for title, image_url in ads %}
        <li>
            <img src="{{ image_url }}" alt="{{ title }}">
            <h2>{{ title }}</h2>
        </li>
        {% endfor %}
    </ul>
</body>
</html>
    ''', ads=ads)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)