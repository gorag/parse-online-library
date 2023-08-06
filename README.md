# Парсер книг с сайта tululu.org

Собирает информацию о книгах с возможностью скачивания.

### Как установить

Скачать парсер с gihub:

`git https://github.com/gorag/parse-online-library.git`

Установить зависимости:
    
`poetry install`

### Аргументы

`--start_id` - id книги с которого начинается парсинг, по умолчанию равно 1.

`--end_id` - id книги на который заканчивается парсинг, по умолчанию равно 10.

`--books_folder` - папка в которую скачиваются книги, по умолчанию `books`

`--images_folder` - папка в которую скачиваются обложки книг, по умолчанию `images`

Пример:

`python3 main.py --start_id 10 --end_id 20`

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).