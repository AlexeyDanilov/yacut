import re
from http import HTTPStatus
from flask import request, jsonify

from . import app, db
from .constants import WRONG_LINK_NAME_MESSAGE, REG_EXPRESSION
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id, DUPLICATE_MESSAGE


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if data is None or not len(data):
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if URLMap.query.filter_by(short=data.get('custom_id')).first():
        raise InvalidAPIUsage(DUPLICATE_MESSAGE)
    if 'custom_id' in data and data.get('custom_id') and len(data.get('custom_id')) > 16:
        raise InvalidAPIUsage(WRONG_LINK_NAME_MESSAGE)
    if 'custom_id' in data and data.get('custom_id') and not re.match(REG_EXPRESSION, data.get('custom_id')):
        raise InvalidAPIUsage(WRONG_LINK_NAME_MESSAGE)
    if 'custom_id' not in data or not data.get('custom_id'):
        short_link = get_unique_short_id()
        while URLMap.query.filter_by(short=short_link).first():
            short_link = get_unique_short_id()

        data['custom_id'] = short_link

    url = URLMap()
    modified_data = dict(
        original=data.get('url'),
        short=data.get('custom_id')
    )
    url.from_dict(modified_data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/')
def get_original_link(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if not link:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)

    return jsonify({'url': link.original}), HTTPStatus.OK
