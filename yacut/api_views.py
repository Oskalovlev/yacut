from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from .functionality import check_allowed_char, get_unique_short_id, check_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!', HTTPStatus.BAD_REQUEST)

    if 'custom_id' not in data or data['custom_id'] is None:
        data['custom_id'] = get_unique_short_id()

    custom_id = data['custom_id']
    if len(custom_id) > 16 or not check_allowed_char(custom_id):
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки',
            HTTPStatus.BAD_REQUEST
        )

    if check_unique_short_id(custom_id):
        raise InvalidAPIUsage((f'Имя "{custom_id}" уже занято.'), HTTPStatus.BAD_REQUEST)

    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short_id(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK
