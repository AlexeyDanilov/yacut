#!/usr/bin/env bash

case "$OSTYPE" in
    msys*)    python=python ;;
    cygwin*)  python=python ;;
    *)        python=python3 ;;
esac

# Путь к директории с models.py
export PYTHONPATH="../"

cd ../
echo "from yacut import db; \
     db.create_all(); \
     from yacut.models import URLMap; \
     URLMap.query.delete(); \
     url_map_object = URLMap(original='https://example.com/', short='example'); \
     db.session.add(url_map_object); \
     db.session.commit()" | flask shell >/dev/null 2>&1
cd -
