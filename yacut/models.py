from datetime import datetime

from flask import url_for

from . import db


class URLMap(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def from_dict(self, data):
        for field in ('original', 'short'):
            setattr(self, field, data.get(field))

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('redirect_link', short_link=self.short, _external=True),
        )
