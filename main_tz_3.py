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

    r = requests.get('https://naturasiberica.ru/our-shops/', headers=headers)
    # создаём объект BeautifulSoup
    soup = BeautifulSoup(r.text, 'lxml')
    new_address = (str(soup.find('ul', class_='card-list').find_all('li')[18].text).split())
    address = f'"{new_address[3]} {new_address[4]} {new_address[5]} {new_address[6]} {new_address[7]} {new_address[8]}'
    create_link = str(soup.find('ul', class_='card-list').find_all('li')[18]).split('/our-shops/')[1].split('/')[0]
    link = f'https://naturasiberica.ru/our-shops/{create_link}/clmap/26812653/'
    time.sleep(2)
    r = requests.get(link, headers=headers)
    # создаём объект BeautifulSoup
    soup = BeautifulSoup(r.text, 'lxml')
    print(soup.find(class_='original-shops__address').text)
    # print(soup.find('div', class_='our-shops__shops original-shops').find_all('div', class_='original-shops__info')[0].text)
    name = str(soup.title.text)[-15::]
    phones = [str(soup.find('div', class_='original-shops__info').find_all('p')[1].text)[9::]]
    working_hours = []
    clock = \
        str(soup.find('div', class_='original-shops__info').find('div',
                                                                 class_='original-shops__schedule').text).split()[-1]
    working_hours.append(f'пн-вс {clock.replace(".", ":")}')
    c = address.split()
    location = geolocator.geocode(f'{(c[0])[1:-1]} {c[1]} {(c[3])[0:-1]}')
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
    with open(f'data/data_tz_3.json', 'a') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    collect_data()


if __name__ == '__main__':
    main()
