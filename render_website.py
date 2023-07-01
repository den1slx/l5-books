from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
import json
import argparse


def on_reload():
    parser = create_parser()
    args = parser.parse_args()
    path = args.path
    with open(path, 'r', encoding='UTF-8') as f:
        books = json.load(f)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    rendered_page = template.render(
        books=books,
    )

    with open('index.html', 'w', encoding="utf8") as file:
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
    server.serve(root='.')
    # http://127.0.0.1:5500/


if __name__ == '__main__':
    main()