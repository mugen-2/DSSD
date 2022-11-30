from os import path, environ, urandom
from flask import Flask, render_template, g, Blueprint, session
from flask_session import Session
from flask_login import LoginManager,current_user
from config import config
from app import db
from app.models.user import User
from app.resources import user, collection, auth, reservaMateriales, espacioFabricacion, planComercial,metricas
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
    app.add_url_rule("/colecciones/detalle/<idcoleccion>", "collection_detalle", collection.detalle)
    app.add_url_rule("/colecciones/<idreserva>", "collection_new_reasignar", collection.newReasingarfecha)
    app.add_url_rule("/colecciones/reasignar/<idreserva>", "collection_reasignar", collection.reasignarFecha,methods=["POST"])
    
    #Rutas Metricas
    app.add_url_rule("/metricas", "metricas_index", metricas.index)
    app.add_url_rule("/metricas/crm", "cantResxMaterial", metricas.cantResxMaterial)

    # Rutas Reserva Materiales
    app.add_url_rule("/reservaMateriales/<idcoleccion>", "reservaMateriales_index", reservaMateriales.index)
    app.add_url_rule("/reservaMateriales/listarMateriales/<idcoleccion>", "listarMateriales", reservaMateriales.list)
    app.add_url_rule("/reservaMateriales/nuevo/<idcoleccion>/<idmaterial>", "reservaMateriales_new", reservaMateriales.new)
    app.add_url_rule("/reservaMateriales/verificar/<idreserva>", "verificarReservaMateriales", reservaMateriales.verificar)
    app.add_url_rule("/reservaMateriales/<idcoleccion>/<idmaterial>", "reservaMateriales_create", reservaMateriales.create, methods=["POST"])

    # Rutas Espacios de Fabricación
    app.add_url_rule("/espacioFabricacion/<idcoleccion>", "espacioFabricacion_index", espacioFabricacion.index)
    app.add_url_rule("/espacioFabricacion/nuevo/<idcoleccion>/<idfabricante>", "espacioFabricacion_new", espacioFabricacion.new)
    app.add_url_rule("/espacioFabricacion/verificar/<idcoleccion>", "verificarFabricacion", espacioFabricacion.verificar)
    app.add_url_rule("/espacioFabricacion/<idcoleccion>/<idfabricante>", "espacioFabricacion_create", espacioFabricacion.create, methods=["POST"])

    # Rutas Plan Comercial
    app.add_url_rule("/planComercial/<idcoleccion>", "planComercial_new", planComercial.new)
    app.add_url_rule("/planComercial/<idcoleccion>", "planComercial_create", planComercial.create, methods=["POST"])
    app.add_url_rule("/planComercial/<idcoleccion>", "planComercial_verificar", planComercial.verificar)
    app.add_url_rule("/planComercial/<idcoleccion>", "planComercial_verificar2", planComercial.verificar2, methods=["POST"])

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        if 'rol' in session.keys():
            rol= session["rol"]
        else:
            rol= ""
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
