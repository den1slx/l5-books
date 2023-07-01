from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        description='Книги')
    parser.add_argument('--path', '-p', help='Path to json file, default: %(default)s',
                        default='books.json')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    path = args.path
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    with open(path, 'r', encoding='UTF-8') as f:
        books = json.load(f)

    rendered_page = template.render(
        books=books,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()