import argparse
import urllib.parse
from pathlib import Path
from pprint import pprint

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests.exceptions import HTTPError
from requests.models import Response

import requests
import urllib3


def check_for_redirect(response: Response) -> None:
    if response.history:
        raise HTTPError


def get_response(url):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(url, verify=False)
    response.raise_for_status()
    check_for_redirect(response)
    return response


def download_file(url, filename, folder):
    """Функция для скачивания файлов.
    Args:
        url (str): Cсылка на файл, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь, куда сохранен файл.
    """
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = get_response(url)
    filepath = Path(folder).joinpath(sanitize_filename(filename))
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def parse_book_page(html):
    soup = BeautifulSoup(html, 'lxml')
    h1 = soup.find('div', id='content').find('h1').text.split('::')
    name = h1[0].strip()
    author = h1[1].strip()
    image_url = urllib.parse.urljoin(
        tululu_url,
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
        "name": name,
        "author": author,
        "image_url": image_url,
        "comments": comments,
        "genres": genres,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_id", type=int, default=1)
    parser.add_argument("--end_id", type=int, default=10)
    parser.add_argument("--books_folder", default="books/")
    parser.add_argument("--images_folder", default="images/")
    args = parser.parse_args()

    tululu_url = "https://tululu.org/"
    book_txt_url = f"{tululu_url}txt.php?id="
    book_page_url = f"{tululu_url}b"

    for i in range(args.start_id, args.end_id + 1):
        book_url = f"{book_txt_url}{i}"
        try:
            book_response = get_response(f"{book_page_url}{i}/")
            book_info = parse_book_page(book_response.text)
            image_name = Path(urllib.parse.urlsplit(book_info['image_url']).path).name
            pprint(book_info)
            download_file(book_url, f"{i}. {book_info['name']}.txt", args.books_folder)
            if image_name != "nopic.gif":
                download_file(book_info['image_url'], image_name, args.images_folder)
        except HTTPError:
            pass
