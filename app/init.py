from os import path, environ, urandom
from flask import Flask, render_template, g, Blueprint
from flask_session import Session
from flask_login import LoginManager
from config import config
from app import db
from app.models.user import User
from app.resources import configuracion, seguimiento, zonas_inundables
from app.resources import user
from app.resources import auth
from app.resources import puntosDeEncuentro
from app.resources import denuncia
from app.resources import recorrido
from app.resources.api.zonaI import zonaI_api
from app.resources.api.denuncia import denuncia_api
from app.resources.api.recorrido import recorridoE_api
from app.resources.api.punto import puntosE_api
from app.resources.api.categorias import categorias_api
from app.helpers import handler
from app.helpers import auth as helper_auth
from oauthlib.oauth2 import WebApplicationClient
from flask_cors import CORS

GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID", "511645563531-euah8nadpcuu1dch1eee0k8n6ifd3cmo.apps.googleusercontent.com")
#GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET", "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")
#GOOGLE_DISCOVERY_URL = (
#    "https://accounts.google.com/.well-known/openid-configuration"
#)

def create_app(environment="development"):

    # Configuración inicial de la app
    app = Flask(__name__)
    #cors = CORS(app, resources={r"/api.*": {"origins": "*"}})
    app.config['CORS_HEADERS'] = 'Content-Type'

    app.secret_key = environ.get("SECRET_KEY") or urandom(24)

    # OAuth 2 client setup
    client = WebApplicationClient(GOOGLE_CLIENT_ID)

    # Manejador de Sesiones
    login_manager = LoginManager()
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Configure db
    db.init_app(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)

    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )
   
    #app.add_url_rule("/loginG", "iniciar_sesionG", auth.loginG)
    #app.add_url_rule(
    #    "/login/callback", "auth_callback", auth.callback, methods=["GET"]
    # )

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        return render_template("home.html")

    # Rutas de API-REST (usando Blueprints)
    api = Blueprint("api", __name__, url_prefix="/api")

    app.register_blueprint(api)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500

    # Retornar la instancia de app configurada
    return app
