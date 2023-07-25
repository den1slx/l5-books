from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import quote
import json
import argparse


def check_filename(filename):
    symbols = ['?', '/', '\\', ':', '*', '"', '<', '>']
    for symbol in symbols:
        filename = filename.replace(symbol, '')
    return filename


def get_static(filename, format_='txt', folder='', cwd=False, img=False, directory='static'):

    if img:
        static = get_static_img(filename, folder, directory, cwd)
        return static
    filename = check_filename(filename)
    if cwd:
        path = str(Path.cwd()).replace('\\', '/')
        static = f'{path}/{directory}/{folder}{filename}.{format_}'
        return static

    static = quote(f'../{directory}/{folder}{filename}.{format_}', encoding='UTF-8')
    return static


def get_static_img(filename, folder, directory, cwd=False):
    if cwd:
        path = str(Path.cwd()).replace('\\', '/')
        static = f'{path}/{directory}/{folder}{filename}'
        return static
    static = quote(f'../{directory}/{folder}{filename}', encoding='UTF-8')
    return static


def create_book_url(book_id):
    book_url = f'https://tululu.org/b{book_id}/'
    return book_url


def get_index_url(num):
    url = f'index{num}.html'
    return url


def get_full_filename(filename,  format_='.txt', folder=''):
    return f'{folder}{filename}{format_}'


def get_pages_count(books):
    pages_count = len(books) // 20
    if len(books) % 20:
        pages_count += 1
    return pages_count


def on_reload():
    parser = create_parser()
    args = parser.parse_args()
    path = args.path

    with open(path, 'r', encoding='UTF-8') as file:
        books = json.load(file)

    pages = chunked(books, 20)

    books_chunks = [chunked(page, 2) for page in pages]

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    env.globals.update({
        'static': get_static,
        'index_url': get_index_url,
        'book_url': create_book_url,
    })
    template = env.get_template('based_template.html')

    for num, books_chunk in enumerate(books_chunks):
        num += 1
        rendered_page = template.render(
            chunks=books_chunk,
            current_page=num,
            pages_count=get_pages_count(books),
        )
        with open(f'pages/index{num}.html', 'w', encoding="utf-8") as file:
            file.write(rendered_page)


def create_parser():
    parser = argparse.ArgumentParser(
        description='Книги')
    parser.add_argument('--path', '-p', help='Path to json file, default: %(default)s',
                        default='media/books.json')

    return parser


def get_book(path):
    with open(path, 'r', encoding='UTF-8') as book_file:
        book = book_file.read()
    return book


def main():
    path = Path.cwd()
    path = Path(f'{path}/pages/'.replace('\\', '/'))
    path.mkdir(parents=True, exist_ok=True)
    on_reload()  # for args.path
    server = Server()
    server.watch('based_template.html', on_reload)
    server.serve(root='')

    # server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    # server.serve_forever()
    # http://127.0.0.1:8000/
    # http://127.0.0.1:5500/


if __name__ == '__main__':
    main()
