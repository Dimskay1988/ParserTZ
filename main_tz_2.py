import json
import os.path
import time
import requests
from bs4 import BeautifulSoup
import os
import lxml
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="ParserTz")


def get_pages():
    links = []
    headers = {
        "User-Agent": "PostmanRuntime/7.29.2",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    r = requests.get('https://som1.ru/shops/', headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    score = soup.find('div', class_='shops-list').find_all('a', class_='btn btn-blue')
    for i in score:
        links.append(f"https://som1.ru/shops/{(str(i)).split('/')[-3]}/")

    return links, headers


def collect_data(links, headers):
    data = []

    for link in links:
        time.sleep(2)
        r = requests.get(link, headers=headers)
        # создаём объект BeautifulSoup
        soup = BeautifulSoup(r.text, 'lxml')
        address = soup.find('table', class_='shop-info-table').find_next('td').find_next('td').find_next('td').text
        name = soup.find('h1').text
        phones = [
            soup.find('table', class_='shop-info-table').find_next('td').find_next('td').find_next('td').find_next(
                'td').find_next('td').find_next('td').text]
        working_hours = [soup.find('table', class_='shop-info-table').find_all('td')[-1].text]
        location = geolocator.geocode(f"{(str(address))[3::]}")
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

    # # создаём папку с файломи
    if not os.path.exists('data'):
        os.mkdir('data')
    # записываем данные в json файл
    with open(f'data/data_tz_2.json', 'a') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    links, headers = get_pages()
    collect_data(links, headers)


if __name__ == '__main__':
    main()
