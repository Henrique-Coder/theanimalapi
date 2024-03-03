from gzip import open as gzopen
from json import load as json_load
from pathlib import Path


dynamic_folder = Path('assets', 'dynamic')


def get_animal_images() -> dict:
    with gzopen(Path(dynamic_folder, 'databases', 'animal_images.json.gz'), 'rt', encoding='utf-8') as f:
        animal_translations = json_load(f)

    return animal_translations


def get_animal_translations() -> dict:
    with gzopen(Path(dynamic_folder, 'databases', 'animal_translations.json.gz'), 'rt', encoding='utf-8') as f:
        animal_images = json_load(f)

    return animal_images


def get_animal_translation(translations: dict, name: str, language: str = None) -> dict:
    if name not in translations:
        return {
            'error': '404',
            'message': 'Animal Not Found'
        }

    if language is None:
        language = 'en-us'

    elif language not in translations[name]:
        return {
            'error': '404',
            'message': 'Language Not Found'
        }

    response = {
        'language': language,
        'name': translations[name][language]
    }
    return response
