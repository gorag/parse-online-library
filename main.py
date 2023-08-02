import urllib.parse
from pathlib import Path
from requests.exceptions import HTTPError
from requests.models import Response

import requests
import urllib3


def download_book(url: str, path: Path) -> None:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(url, verify=False)
    response.raise_for_status()
    check_for_redirect(response)
    with open(path, 'wb') as file:
        file.write(response.content)


def check_for_redirect(response: Response) -> None:
    if response.history:
        raise HTTPError


if __name__ == '__main__':
    book_directory = Path('books')
    book_id_url = "https://tululu.org/txt.php?id="

    book_directory.mkdir(parents=True, exist_ok=True)
    for i in range(1, 11):
        book_path = Path(f"{book_directory}/id{i}.txt")
        book_url = f"{book_id_url}{i}"

        try:
            download_book(book_url, book_path)
        except HTTPError:
            continue
