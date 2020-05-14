import csv
import re

from datetime import datetime
from pymongo import MongoClient
from pymongo.collation import Collation


def read_data(csv_file, db):

    with open(csv_file, encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            day = row['Дата'].split('.')
            if len(day[0]) == 1:
                day[0] = '0' + day[0]
            date = f'{datetime.now().year}-{day[1]}-{day[0]}'
            row['Дата'] = datetime.fromisoformat(date)
            db.artists_in_town_N.insert_one(row)


def find_cheapest(db):
    return db.artists_in_town_N.find().sort('Цена').collation(Collation(locale='en_US', numericOrdering=True))


def find_by_name(name, db):
    regex = re.compile(name, re.IGNORECASE)
    query = db.artists_in_town_N.find({'Исполнитель': {'$in': [regex]}})
    return query.sort('Цена').collation(Collation(locale='en_US', numericOrdering=True))


def find_by_date(date, db):
    start, end = [datetime.fromisoformat(x) for x in date]
    return db.artists_in_town_N.find({'Дата': {'$gte': start, '$lte': end}}).sort('Дата')


if __name__ == '__main__':
    client = MongoClient()

    database = client['concerts_db']

    read_data('artists.csv', database)

    print('Сортировка по возрастанию цены:')
    for doc in find_cheapest(database):
        print(doc)
    print()

    print('Поиск по имени исполнителя:')
    for doc in find_by_name('t', database):
        print(doc)
    print()

    print('Поиск по дате:')
    for doc in find_by_date(['2020-07-01', '2020-07-30'], database):
        print(doc)
