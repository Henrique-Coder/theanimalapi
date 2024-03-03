from flask import Flask, render_template, jsonify, redirect, url_for
from typing import Union
from pathlib import Path


app = Flask(__name__)
app.app_context().push()
api_versions = tuple(('v1',))

from resources.api.v1.routes import search_v1


@app.errorhandler(404)
def error_404(error) -> jsonify:
    return jsonify({'error': 'Page not found'}), 404


@app.route('/')
def home() -> redirect:
    return redirect(url_for('api_docs'))


@app.route('/api/docs')
def api_docs() -> Union[redirect, render_template]:
    return redirect('/api/docs', 301) and render_template('api_documentation.html')


@app.route('/api/<path:path>')
def catch_wrong_version(path: str) -> jsonify:
    if not any(path.startswith(version) for version in api_versions):
        return jsonify({'message': 'Invalid API version', 'available_versions': api_versions}), 404
    else:
        return jsonify({'message': 'API working successfully! See /api/docs for documentation.'}), 200


def configure_app() -> None:
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB
    app.config['STATIC_FOLDER'] = Path('assets/static')
    app.config['TEMPLATE_FOLDER'] = Path('templates')


if __name__ == '__main__':
    configure_app()
    app.run(debug=False, threaded=True, host='0.0.0.0')
