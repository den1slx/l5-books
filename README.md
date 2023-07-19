## Библиотека

### _О проекте_
* [Библиотека](https://den1slx.github.io/l5-books/)
* [Источник](https://tululu.org)


### _Установка_
- python3 должен быть установлен.
- Скачайте код.
- Установите зависимости командой:
```commandline
pip install -r requirements.txt
```



### _Использование_
* Скачайте книги, картинки и `json` файл следуя [этой](https://github.com/den1slx/l3-books/blob/main/README.md) инструкции.
* Поместите скачанные images и books в папку static
* Поместите скачанный `json` файл рядом с `render_website.py`
* Запустите скрипт командой:
    ```commandline
    python render_website.py --path 'books.json'
    ```

* Сайт будет находиться [здесь](http://127.0.0.1:5500)
* Также можно открыть `index.html` Там не будет странных символов вместо текста


### _Цель проекта_
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).