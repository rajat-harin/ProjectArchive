import os

from flask import (Flask, render_template)
from flaskr.auth import login_required
from flaskr.config import DevelopmentConfig

def create_app(test_config = None):
    #create and config app
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_object(DevelopmentConfig)

    if test_config is None:
        #load instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple index route
    @app.route('/')
    def landing():
        return render_template('/landing.html')
    

    from . import (auth,anime)
    app.register_blueprint(auth.bp)
    app.register_blueprint(anime.bp)

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('/dashboard.html')

    return app