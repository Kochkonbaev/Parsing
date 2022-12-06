from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine, MetaData, Table, Column, Text, Integer, select

engine = create_engine('sqlite:///booking_sqlalhemy.db')

connection = engine.connect()

metadata = MetaData()

houses = Table('houses', metadata,
        Column('houses_id', Integer, primary_key=True),
        Column('image', Text),
        Column('price', Text),
        Column('date_of_publish', Text)
        )

metadata.create_all(engine)

url = "https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273"
page =  requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
lists = soup.find_all('div', class_="search-item")

for list in lists:
    insertion_query = houses.insert().values({
        'image':f"{list.find('img').get('data-src')}",
        'price':f"{list.find('div', class_='price').getText().strip()}",
        'date_of_publish':f"{list.find('span', class_='date-posted').text.strip()}"
    })
    connection.execute(insertion_query)

select_houses_query = select([houses])
select_houses_result = connection.execute(select_houses_query)

print(select_houses_result.fetchall())