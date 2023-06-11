# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from psycopg2 import connect

class ScraperPipeline:

    def __init__(self):
        self.connection = connect(
            host='127.0.0.1',
            port=5432,
            dbname='sreality',
            user='sreality_user',
            password='sreality_password'
        )
        self.cur = self.connection.cursor()
        # Create quotes table if none exists
        self.cur.execute('DROP TABLE IF EXISTS ads;')
        self.cur.execute('CREATE TABLE ads (id SERIAL PRIMARY KEY, title TEXT, image_url TEXT);')
        print('TABLE was created.')
        self.cur.execute('DELETE FROM ads *')


    def process_item(self, item, spider):
        self.cur.execute('''INSERT INTO ads (title, image_url) values (%s,%s)''', (item["title"], str(item["image_url"])))
        self.connection.commit()
        print('ITEM was processed.')
        return item

    def close_spider(self, spider):
        # Make html page for server
        self.cur.execute('''SELECT * FROM ads''')
        print('Selecting rows from ads table')
        ads_records = self.cur.fetchall()
        print("Every row and its columns values")
        for row in ads_records:
            print(f'Title = {row[1]}')
            print(f'Image urls = {row[2]}, "\n"')

        strTable = "<html><meta charset=\"UTF-8\"><table><tr><th>Flats</th><th> </th></tr>"
        for row in ads_records:
            strRW = "<tr><td>" + row[1] + "</td><td><img src=\"" + row[2] + "\"></td></tr>"
            strTable = strTable + strRW

        strTable = strTable + "</table></html>"

        flats = open("../../flats.html", 'w')
        flats.write(strTable)
        flats.close()

        # Close cursor and connection to database
        self.cur.close()
        self.connection.close()
