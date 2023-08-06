import argparse
import logging
import time
import urllib.parse
from pathlib import Path

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests.exceptions import HTTPError, ConnectionError
from requests.models import Response

import requests
import urllib3


def check_for_redirect(response: Response) -> None:
    if response.history:
        raise HTTPError


def get_response(url, params=None):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(url, verify=False, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    return response


def download_file(url, filename, folder, params=None):
    """Функция для скачивания файлов.
    Args:
        url (str): Cсылка на файл, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
        params (dict): Параметры запроса.
    Returns:
        str: Путь, куда сохранен файл.
    """
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = get_response(url, params=params)
    filepath = Path(folder).joinpath(sanitize_filename(filename))
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def parse_book_page(html, page_url):
    soup = BeautifulSoup(html, 'lxml')
    name, author = soup.find('div', id='content').find('h1').text.split('::')
    image_url = urllib.parse.urljoin(
        page_url,
        soup.find('div', class_='bookimage').find('img')['src']
    )
    comments = [
        comment.find('span', class_='black').text
        for comment in soup.find_all('div', class_='texts')
    ]
    genres = [
        genre.text
        for genre in soup.find('span', class_='d_book').find_all('a')
    ]
    return {
        "name": name.strip(),
        "author": author.strip(),
        "image_url": image_url,
        "comments": comments,
        "genres": genres,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Parse online library")
    parser.add_argument("--start_id", type=int, default=1, help="Start book id")
    parser.add_argument("--end_id", type=int, default=10, help="End book id")
    parser.add_argument("--books_folder", default="books/", help="Books download folder")
    parser.add_argument("--images_folder", default="images/", help="Images download folder")
    args = parser.parse_args()

    tululu_url = "https://tululu.org/"
    book_txt_url = f"{tululu_url}txt.php"
    book_page_url = f"{tululu_url}b"

    for book_id in range(args.start_id, args.end_id + 1):
        book_params = {"id": book_id}
        timeout_connection = 1
        error = True
        while error:
            try:
                book_response = get_response(f"{book_page_url}{book_id}/")
                book = parse_book_page(book_response.text, book_response.url)
                image_name = Path(urllib.parse.urlsplit(book['image_url']).path).name
                download_file(
                    book_txt_url,
                    f"{book_id}. {book['name']}.txt",
                    args.books_folder,
                    params=book_params)
                if image_name != "nopic.gif":
                    download_file(book['image_url'], image_name, args.images_folder)
            except ConnectionError:
                logging.error("No internet connection")
                time.sleep(timeout_connection)
                timeout_connection = 5
            except HTTPError:
                logging.warning(f"No book text with id: {book_id}")
                error = False
            else:
                error = False
