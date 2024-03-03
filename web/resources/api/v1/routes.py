from resources.api.v1.functions import IPRequestTimeout
from resources.api.v1.app_data import get_animal_images, get_animal_translations, get_animal_translation
from flask import current_app, request, jsonify, Response, json
from PIL import Image
from httpx import get
from io import BytesIO
from random import choice
from typing import Union


app = current_app

animal_images = get_animal_images()
animal_translations = get_animal_translations()

url_path = animal_images['path']
image_ext = 'jpg'


@app.route('/api/v1/<search>/<animal>')
def search_v1(search: str, animal: str) -> Union[jsonify, Response]:
    if not IPRequestTimeout.check_ip():
        return jsonify({'error': '429', 'message': 'Too Many Requests', 'tip': 'Wait a second and try again'}), 429

    if search != 'search':
        return jsonify({'error': '400', 'message': 'Invalid Function', 'tip': 'Try using /api/v1/search/... and read the documentation'}), 400

    if animal != 'animal':
        return jsonify({'error': '400', 'message': 'Invalid Endpoint', 'tip': 'Try using /api/v1/animal?... and read the documentation'}), 400

    result_name = request.args.get('name')
    result_id = request.args.get('id')
    result_lang = request.args.get('lang')

    if result_name is None:
        result_name = choice(list(animal_images['animals'].keys()))

    elif result_name not in animal_images['animals']:
        return jsonify({'error': '404', 'message': 'Animal Not Found'}), 404

    else:
        result_name = request.args['name']

    if result_id is None:
        result_id = choice(list(animal_images['animals'][result_name].keys()))

    elif not result_id.isnumeric():
        return jsonify({'error': '400', 'message': 'Invalid ID'}), 400

    result_id = f'{int(result_id):07d}'
    if result_id not in animal_images['animals'][result_name]:
        return jsonify({'error': '404', 'message': 'ID Not Found'}), 404

    image_url = f'{url_path}/{result_name}/{result_name}-{result_id}.{image_ext}'

    try:
        image_content = get(image_url).content
        image_width, image_height = Image.open(BytesIO(image_content)).size
    except Exception:
        return jsonify({'error': '404', 'message': 'Image could not be loaded'}), 404

    response = {
        'id': result_id,
        'name': result_name,
        'translation': get_animal_translation(animal_translations, result_name, result_lang),
        'size': len(image_content),
        'width': image_width,
        'height': image_height,
        'url': image_url
    }
    json_response = Response(json.dumps(response, ensure_ascii=False), content_type='application/json; charset=utf-8')

    return json_response
