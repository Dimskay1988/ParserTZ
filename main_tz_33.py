import json
import os.path
import time
from bs4 import BeautifulSoup
import os
import lxml
from selenium import webdriver
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="ParserTz")


def selenium_get():
    driver = webdriver.Chrome(executable_path='/Users/anikeenko/PycharmProjects/ParserTZ/data/chromedriver')
    driver.maximize_window()

    try:
        driver.get("https://naturasiberica.ru/our-shops/maroseyka/")
        time.sleep(3)

        # создаём папку с файломи
        if not os.path.exists('data'):
            os.mkdir('data')

        # Сохраняем страницы
        with open('data/page_33.html', 'w') as file:
            file.write(driver.page_source)

    except Exception as es:
        print(es)

    finally:
        driver.close()
        driver.quit()


def collect_data():
    data = []

    # прочитать сохраннённую страницу
    with open('data/page_33.html') as file:
        src = file.read()
    # создаём объект BeautifulSoup
    soup = BeautifulSoup(src, 'lxml')
    new_address = (str(soup.find('ul', class_='card-list').find_all('li')[18].text).split())
    address = f'"{new_address[3]} {new_address[4]} {new_address[5]} {new_address[6]} {new_address[7]} {new_address[8]}'
    # создаём объект BeautifulSoup
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

    # записываем данные в json файл
    with open(f'data/data_tz_33.json', 'a') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    selenium_get()
    collect_data()


if __name__ == '__main__':
    main()
