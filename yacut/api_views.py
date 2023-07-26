from http import HTTPStatus

from flask import jsonify, request

from . import app
from .models import URLMap
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!', HTTPStatus.BAD_REQUEST)

    return jsonify(URLMap.save(
        data['url'],
        data.get('custom_id'),
        validate=True
    ).to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_short_id(short):
    url = URLMap.get(short)
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK
