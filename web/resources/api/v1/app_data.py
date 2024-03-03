from gzip import open as gzopen
from json import load as jsload
from pathlib import Path


# Folders
dynamic_folder = Path('assets', 'dynamic')


def get_animal_images():
    with gzopen(Path(dynamic_folder, 'databases', 'animal_images.json.gz'), 'rt', encoding='utf-8') as f:
        animal_translations = jsload(f)
    return animal_translations


def get_animal_translations():
    with gzopen(Path(dynamic_folder, 'databases', 'animal_translations.json.gz'), 'rt', encoding='utf-8') as f:
        animal_images = jsload(f)
    return animal_images

    # {
    #     "antelope": {
    #         "en-us": "Antelope",
    #         "pt-br": "Antílope",
    #         "es-mx": "Antílope",
    #         "fr-fr": "Antilope",
    #         "de-de": "Antilope",
    #         "it-it": "Antilope",
    #         "ja-jp": "アンテロープ",
    #         ...
    #     },
    #     ...
    # }


def get_animal_translation(translations, name, language):
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
