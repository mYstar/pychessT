import os

from flask import Flask, send_from_directory


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_url_path='/static', static_folder='static')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'chesst.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    @app.route('/<filename>.png')
    def serve_png(filename):
        return send_from_directory('static', f'{filename}.png', mimetype='image/png')

    @app.route('/<filename>.svg')
    def serve_svg(filename):
        return send_from_directory('static', f'{filename}.svg', mimetype='image/svg+xml')

    @app.route('/<filename>.ttf')
    def serve_ttf(filename):
        return send_from_directory('static', f'{filename}.ttf', mimetype='application/font-sfnt')

    @app.route('/<filename>.woff2')
    def serve_woff2(filename):
        return send_from_directory('static', f'{filename}.woff2', mimetype='application/woff2')

    @app.route('/<filename>.woff')
    def serve_woff(filename):
        return send_from_directory('static', f'{filename}.woff', mimetype='application/font-woff')

    from . import auth
    app.register_blueprint(auth.bp)

    from . import game
    app.register_blueprint(game.bp)
    app.add_url_rule('/', endpoint='index')

    return app
