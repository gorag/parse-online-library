from pathlib import Path

import requests
import urllib3


def download_book(url: str, directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    for i in range(1, 11):
        url = f"{url}{1}"
        response = requests.get(url, verify=False)
        response.raise_for_status()
        path = Path(f"{directory}/id{i}.txt")
        with open(path, 'wb') as file:
            file.write(response.content)


def check_for_redirect(response):
    return response


if __name__ == '__main__':
    book_url = "https://tululu.org/txt.php?id="
    download_book(book_url, Path('books'))
