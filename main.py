import os.path
from pathlib import Path
from pprint import pprint

import requests
import urllib3


def download_book(url: str, path: Path) -> None:
    parent_path = path.parent
    parent_path.mkdir(parents=True, exist_ok=True)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(url, verify=False)
    response.raise_for_status()

    pprint(response.text)

    # with open(path, 'wb') as file:
    #     file.write(response.content)


def check_for_redirect(response):
    return response


if __name__ == '__main__':
    # book_url = "https://tululu.org/txt.php?id=32168"
    book_url = "https://tululu.org/b32168/"
    download_book(book_url, Path('books/book1.txt'))
