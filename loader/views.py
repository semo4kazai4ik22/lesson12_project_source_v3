import logging

from flask import Blueprint, render_template, request
from loader.utils import save_picture
from functions import add_post
from json import JSONDecodeError


loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates')

@loader_blueprint.route('/post')
def post_page():
    return render_template('post_form.html')


@loader_blueprint.route('/post', methods=['POST'])
def add_post_page():
    picture = request.files.get('picture')
    content = request.form.get('content')

    if not picture or not content:
        return f"Нет картинки/текста"
    if picture.filename.split('.')[-1] not in ['jpeg', 'png']:
        logging.info("Загруженный файл не картинка")
        return "Неверное расширение файла"

    try:
        picture_path: str = '/' + save_picture(picture)
    except FileNotFoundError:
        return "Файл не найден, пуся"
    except JSONDecodeError:
        return "Невалидный файл"
    post: dict = add_post({'pic': picture_path, 'content': content})
    return render_template('post_uploaded.html', post=post)

