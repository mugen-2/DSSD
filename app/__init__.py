from os import path, environ, urandom
from flask import Flask, render_template, g, Blueprint, session
from flask_session import Session
from flask_login import LoginManager
from config import config
from app import db
from app.models.user import User
from app.resources import user, collection, auth, reservaMateriales
#from app.resources import auth
from app.helpers import handler
from app.helpers import auth as helper_auth
from oauthlib.oauth2 import WebApplicationClient

GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID", "511645563531-euah8nadpcuu1dch1eee0k8n6ifd3cmo.apps.googleusercontent.com")

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

    # Rutas Usuarios
    app.add_url_rule("/usuarios", "user_index", user.index)
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    app.add_url_rule("/usuarios/borrar/<user_id>", "user_delete", user.delete, methods=["POST"] )

    # Rutas Collection
    app.add_url_rule("/colecciones", "collection_index", collection.index)
    app.add_url_rule("/colecciones", "collection_create", collection.create, methods=["POST"])
    app.add_url_rule("/colecciones/nuevo", "collection_new", collection.new)

    # Rutas Reserva Materiales
    app.add_url_rule("/reservaMateriales/<idcoleccion>", "reservaMateriales_index", reservaMateriales.index)
    app.add_url_rule("/reservaMateriales/listarMateriales/<idcoleccion>", "listarMateriales", reservaMateriales.list)
    app.add_url_rule("/reservaMateriales/nuevo/<idcoleccion>/<cantidad>", "reservaMateriales_new", reservaMateriales.new)
    app.add_url_rule("/reservaMateriales/<idcoleccion>", "reservaMateriales_create", reservaMateriales.create, methods=["POST"])

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        rol= session["rol"]
        #print(rol)
        return render_template("home.html",rol=rol)

    # Rutas de API-REST (usando Blueprints)
    #api = Blueprint("api", __name__, url_prefix="/api")

    #app.register_blueprint(api)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500

    # Retornar la instancia de app configurada
    return app
