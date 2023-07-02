from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

from pathlib import Path
from urllib.parse import quote
import json
import argparse


def get_static(filename, format_='txt', folder=''):
    # path = Path().cwd()
    # correct_path = str(path).replace('\\', '/')
    # static = f'file:///{correct_path}/static/{book_title}.{format_}'
    # static = quote(static, safe='/:', encoding='UTF-8')
    static = quote(f'/static/{folder}{filename}.{format_}', encoding='UTF-8')
    return static


def create_book_url(book_id):
    book_url = f'https://tululu.org/b{book_id}/'
    return book_url


def get_url(filename):
    url = None
    return url


def on_reload():
    parser = create_parser()
    args = parser.parse_args()
    path = args.path
    with open(path, 'r', encoding='UTF-8') as f:
        books = json.load(f)

    pages = chunked(books, 20)

    books_chunks = [chunked(page, 2) for page in pages]

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    env.globals.update({
        'static': get_static,
        'url': get_url,
        'book_url': create_book_url,
    })
    template = env.get_template('templates/based_template.html')

    for num, books_chunk in enumerate(books_chunks):
        rendered_page = template.render(
            chunks=books_chunk,
        )

        with open(f'templates/index_{num}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


def create_parser():
    parser = argparse.ArgumentParser(
        description='Книги')
    parser.add_argument('--path', '-p', help='Path to json file, default: %(default)s',
                        default='books.json')
    return parser


def main():
    on_reload()  # for args.path
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='templates/')
    # http://127.0.0.1:5500/


if __name__ == '__main__':
    main()