# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from psycopg2 import connect

class ScraperPipeline:

    def __init__(self):
        self.connection = connect(
            host='db',
            port=5432,
            dbname='sreality',
            user='sreality_user',
            password='sreality_password'
        )
        self.cur = self.connection.cursor()
        # Create table if none exists
        self.cur.execute('DROP TABLE IF EXISTS ads')
        self.cur.execute('CREATE TABLE ads (id SERIAL PRIMARY KEY, title TEXT, image_url TEXT)')
        print('TABLE was created.')
        self.cur.execute('DELETE FROM ads *')


    def process_item(self, item, spider):
        self.cur.execute('''INSERT INTO ads (title, image_url) values (%s,%s)''', (item["title"].encode('latin1').decode('utf8'), item["image_url"]))
        self.connection.commit()
        print('ITEM was processed.')
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()