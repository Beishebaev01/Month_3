import requests
from bs4 import BeautifulSoup

URL = "https://github.com/Beishebaev01"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}


def get_html(url):
    response = requests.get(url=url, headers=HEADERS)
    return response


def get_data_from_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all(
        'li', class_="mb-3 d-flex flex-content-stretch col-12 col-md-6 col-lg-6"
    )
    repositories = []
    for item in items:
        repos = {
            "1. Репозиторий": item.find(
                'div',
                class_="d-flex width-full flex-items-center position-relative"
            ).find('a').getText(strip="\n"),
            "2. Коды": "https://github.com" + item.find(
                'div',
                class_="d-flex width-full flex-items-center position-relative"
            ).find('a').get("href"),
            "3. Язык": item.find(
                'p',
                class_="mb-0 f6 color-fg-muted"
            ).find('span', class_="d-inline-block mr-3").getText(strip="\n")
        }
        repositories.append(repos)

    return repositories


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        repositories = []
        current_page = get_data_from_page(html.text)
        repositories.extend(current_page)
        return repositories
    else:
        raise Exception("ERROR IN PARSER")
