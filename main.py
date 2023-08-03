import urllib.parse
from pathlib import Path

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests.exceptions import HTTPError
from requests.models import Response

import requests
import urllib3


def download_txt(url, filename, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    Path(folder).mkdir(parents=True, exist_ok=True)

    response = get_response(url)

    filepath = Path(folder).joinpath(sanitize_filename(f"{filename}.txt"))

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def check_for_redirect(response: Response) -> None:
    if response.history:
        raise HTTPError


def get_response(url):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(url, verify=False)
    response.raise_for_status()
    check_for_redirect(response)
    return response


if __name__ == '__main__':
    book_id_url = "https://tululu.org/txt.php?id="
    book_page_url = "https://tululu.org/b"

    # print(soup.find('div', class_='bookimage').find('img')['src'])

    for i in range(1, 11):
        book_url = f"{book_id_url}{i}"

        try:
            response = get_response(f"{book_page_url}{i}/")
            soup = BeautifulSoup(response.text, 'lxml')
            book_name = soup.find('div', id='content').find('h1').text.split('::')[0].strip()
            download_txt(book_url, f"{i}. {book_name}")
        except HTTPError:
            continue
