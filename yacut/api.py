from http import HTTPStatus

from flask import request, jsonify

from . import app
from .error_handlers import InvalidAPIUsage, CreateLinkException
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if data is None or not len(data):
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    try:
        url = URLMap.create_link(data)
    except CreateLinkException as e:
        raise InvalidAPIUsage(e.args[0])
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/')
def get_original_link(short_id):
    link = URLMap.get_link(short_id)
    if not link:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)

    return jsonify({'url': link.original}), HTTPStatus.OK
