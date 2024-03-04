import random
import re
import string
from datetime import datetime

from flask import url_for

from . import db
from .constants import (
    DUPLICATE_MESSAGE,
    WRONG_LINK_NAME_MESSAGE,
    REG_EXPRESSION,
    MAX_LENGTH_URL,
    MAX_LENGTH_SHORT_ID,
    REDIRECT_URL
)
from .error_handlers import InvalidAPIUsage


class URLMap(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_URL), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT_ID), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def from_dict(self, data):
        for field in ('original', 'short'):
            setattr(self, field, data.get(field))

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(REDIRECT_URL, short_link=self.short, _external=True),
        )

    @staticmethod
    def create_link(data):
        if URLMap.get_link(data.get('custom_id')):
            raise InvalidAPIUsage(DUPLICATE_MESSAGE)
        if 'custom_id' in data and data.get('custom_id') and len(data.get('custom_id')) > 16:
            raise InvalidAPIUsage(WRONG_LINK_NAME_MESSAGE)
        if 'custom_id' in data and data.get('custom_id') and not re.match(REG_EXPRESSION, data.get('custom_id')):
            raise InvalidAPIUsage(WRONG_LINK_NAME_MESSAGE)
        if 'custom_id' not in data or not data.get('custom_id'):
            short_link = URLMap.get_unique_short_id()
            data['custom_id'] = short_link

        url = URLMap()
        modified_data = dict(
            original=data.get('url') or data.get('original_link'),
            short=data.get('custom_id')
        )
        url.from_dict(modified_data)
        db.session.add(url)
        db.session.commit()
        return url

    @staticmethod
    def get_link(short_id):
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def get_unique_short_id():
        short_link = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        while URLMap.query.filter_by(short=short_link).first():
            short_link = URLMap.get_unique_short_id()

        return short_link
