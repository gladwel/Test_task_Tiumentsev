from flask import Flask, render_template_string
from psycopg2 import connect
import json

app = Flask(__name__)

db_conn = connect(
    host='127.0.0.1',
    port=5432,
    dbname='sreality',
    user='sreality_user',
    password='sreality_password'
)

# file = open('../scraper/pretty_flats.json', 'r')
# items = json.load(file)
#
# with db_conn:
#     with db_conn.cursor() as cur:
#         cur.execute('DROP TABLE IF EXISTS ads;')
#         cur.execute('CREATE TABLE ads (id SERIAL PRIMARY KEY, title VARCHAR(255), image_url TEXT);')
#
#         for item in items:
#             cur.execute('INSERT INTO ads (title, image_url) VALUES (%s, %s);',
#                         (item['title'], item['image_url']))

@app.route('/')
def index():
    with db_conn:
        with db_conn.cursor() as cur:
            cur.execute("SELECT title, image_url FROM ads")
            ads = cur.fetchall()

    return render_template_string('''
        <!doctype html>
        <html>
        <body>
            <h1>Scraped ads</h1>
            <ul>
            {% for title, image_url in ads %}
                <li>
                    <h2>{{ title }}</h2>
                    <img src="{{ image_url }}" alt="{{ title }}"/>
                </li>
            {% endfor %}
            </ul>
        </body>
        </html>
    ''', ads=ads)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)