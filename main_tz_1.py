import json
import os.path
import time
import requests
from bs4 import BeautifulSoup
import os
import lxml
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="ParserTz")


def collect_data():
    headers = {
        "User-Agent": "PostmanRuntime/7.29.2",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    data = []

    r = requests.get('https://oriencoop.cl/sucursales.htm', headers=headers)
    # создаём объект BeautifulSoup
    soup = BeautifulSoup(r.text, 'lxml')
    create_link = soup.find('div', class_='c-left').find_all('a')[5]
    time.sleep(2)
    link = f"https://oriencoop.cl/sucursales/{((str(create_link)).split('/')[-2])[:3]}"
    r = requests.get(link, headers=headers)
    # создаём объект BeautifulSoup
    soup = BeautifulSoup(r.text, 'lxml')
    address = soup.find('div', class_='s-dato').find('p').find('span').text
    name = str(soup.title.text)[-9::]
    phones = []
    phones.append(soup.find('div', class_='s-dato').find_next('p').find_next('p').find('span').text)
    phones.append(soup.find('div', class_='t-content t-session').find_all('li', class_='call')[-2].text)
    phones.append(soup.find('div', class_='t-content t-session').find_all('li', class_='call')[-1].text)
    working_hours = []
    clok = [str(soup.find('div', class_='s-dato').find_all('p')[-1].find_all('span')[0].text).replace('.', ':').split(' '), str(soup.find('div', class_='s-dato').find_all('p')[-1].find_all('span')[1].text).replace('.', ':').split(' ')]
    working_hours.append(f'mon-thu {clok[0][2]} - {clok[0][4]} {clok[1][2]}-{clok[1][4]}')
    working_hours.append(f'fri {clok[0][2]} - {clok[0][4]} {clok[1][2]}-{clok[1][4]}')
    location = geolocator.geocode(f"{address.split('-')[0]}{address.split('-')[1]}")
    latlon = [location.longitude, location.latitude]

    data.append(
        {
            'address': address,
            'latlon': latlon,
            'name': name,
            'phones': phones,
            "working_hours": working_hours
        }
    )

    # создаём папку с файломи
    if not os.path.exists('data'):
        os.mkdir('data')
    # записываем данные в json файл
    with open(f'data/data_tz_1.json', 'a') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    collect_data()


if __name__ == '__main__':
    main()
