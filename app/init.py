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
    cors = CORS(app, resources={r"/api.*": {"origins": "*"}})
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
   
    app.add_url_rule("/loginG", "iniciar_sesionG", auth.loginG)
    app.add_url_rule(
        "/login/callback", "auth_callback", auth.callback, methods=["GET"]
    )
    #app.add_url_rule(
    #    "/login/bienvenido", "auth_bienvenido", auth.bienvenido, methods=["GET"]
    #)

    # Rutas de Consultas
    #app.add_url_rule("/consultas", "issue_index", issue.index)
    #app.add_url_rule("/consultas", "issue_create", issue.create, methods=["POST"])
    #app.add_url_rule("/consultas/nueva", "issue_new", issue.new)

    # Rutas de Usuarios
    app.add_url_rule("/usuarios", "user_index", user.index)
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    app.add_url_rule("/usuarios/editar/<user_id>", "user_update", user.update, methods=["POST"])
    app.add_url_rule("/usuarios/new_editar/<user_id>", "user_new_edit", user.new_update)
    app.add_url_rule("/usuarios/borrar/<user_id>", "user_delete", user.delete, methods=["POST"] )
    app.add_url_rule("/usuarios/bloquear/<user_id>", "user_block", user.block, methods=["POST"] )
    app.add_url_rule("/usuarios/nuevo/asignar_rol/<user_id>", "new_user_assign_rol", user.new_assign_rol)
    app.add_url_rule("/usuarios/asignar_rol/<user_id>/<rol_id>", "user_assign_rol", user.assign_rol)
    app.add_url_rule("/usuarios/desasignar_rol/<user_id>/<rol_id>", "user_unassign_rol", user.unassign_rol)
    app.add_url_rule("/usuarios/search", "user_search", user.search, methods=["POST"])
    app.add_url_rule("/usuarios/confirmUsers", "user_confirm_users", user.confirmarUsuarios)
    app.add_url_rule("/usuarios/confirm/<user_id>", "user_confirm", user.confirmar, methods=["POST"] )
    


    # Rutas de Puntos de Encuentro
    app.add_url_rule("/puntosDeEncuentro", "puntosDeEncuentro_index", puntosDeEncuentro.index)
    app.add_url_rule("/puntosDeEncuentro", "puntosDeEncuentro_create", puntosDeEncuentro.create, methods=["POST"])
    app.add_url_rule("/puntosDeEncuentro/nuevo", "puntosDeEncuentro_new", puntosDeEncuentro.new) 
    app.add_url_rule("/puntosDeEncuentro/show/<puntoDeEncuentro_id>","puntosDeEncuentro_show", puntosDeEncuentro.show)
    app.add_url_rule("/puntosDeEncuentro/delete/<puntoDeEncuentro_id>", "puntosDeEncuentro_delete", puntosDeEncuentro.delete, methods=["POST"])
    app.add_url_rule("/puntosDeEncuentro/update/<puntoDeEncuentro_id>", "puntosDeEncuentro_update", puntosDeEncuentro.update, methods=["POST"])
    app.add_url_rule("/puntosDeEncuentro/new_update/<puntoDeEncuentro_id>", "puntoDeEncuentro_new_update", puntosDeEncuentro.new_update, methods=["POST"])
    app.add_url_rule("/puntosDeEncuentro/search", "puntosDeEncuentro_search", puntosDeEncuentro.search, methods=["POST"])



    # Rutas de Denuncias
    app.add_url_rule("/denuncia", "denuncia_index", denuncia.index)
    app.add_url_rule("/denuncia", "denuncia_create", denuncia.create, methods=["POST"])
    app.add_url_rule("/denuncia/nuevo", "denuncia_new", denuncia.new) 
    app.add_url_rule("/denuncia/show/<denuncia_id>","denuncia_show", denuncia.show)
    app.add_url_rule("/denuncia/delete/<denuncia_id>", "denuncia_delete", denuncia.delete, methods=["POST"])
    app.add_url_rule("/denuncia/update/<denuncia_id>", "denuncia_update", denuncia.update, methods=["POST"])
    app.add_url_rule("/denuncia/new_update/<denuncia_id>", "denuncia_new_update", denuncia.new_update, methods=["POST"])
    app.add_url_rule("/denuncia/search", "denuncia_search", denuncia.search, methods=["POST"])
    
    
    
    # Rutas de Configuracion
    app.add_url_rule("/configuracion", "configuracion_newconfig", configuracion.newconfig)
    app.add_url_rule("/configuracionConfirmada", "configuracion_config", configuracion.config, methods=["POST"])

    # Rutas de Recorridos
    app.add_url_rule("/recorridos", "recorrido_index", recorrido.index)
    app.add_url_rule("/recorrido","recorrido_create",recorrido.create,methods=["POST"])
    app.add_url_rule("/recorridos/new","recorrido_new",recorrido.new)
    app.add_url_rule("/recorridos/show/<recorrido_id>","recorrido_show",recorrido.show)
    app.add_url_rule("/recorridos/delete/<recorrido_id>","recorrido_delete",recorrido.delete,methods=["POST"])
    app.add_url_rule("/recorrido/search", "recorrido_search", recorrido.search, methods=["POST"])
    app.add_url_rule("/recorrido/new_editar/<recorrido_id>", "recorrido_new_edit", recorrido.new_update,methods=["POST"])
    app.add_url_rule("/recorrido/editar/<recorrido_id>", "recorrido_update", recorrido.update, methods=["POST"])
    app.add_url_rule("/recorrido/despublicar/<recorrido_id>", "recorrido_unpublish", recorrido.unpublish, methods=["POST"] )

    # Rutas de Zonas Inundables
    app.add_url_rule("/zonas", "zonas_index", zonas_inundables.index)
    app.add_url_rule("/zonas", "zonas_create", zonas_inundables.create, methods=["POST"])
    app.add_url_rule("/zonasCSV", "zonas_createCSV", zonas_inundables.createCSV, methods=["POST"])
    app.add_url_rule("/zonas/nuevo", "zonas_new", zonas_inundables.new)
    app.add_url_rule("/zonas/importar", "zonas_newCSV", zonas_inundables.newCSV) 
    app.add_url_rule("/zonas/<zona_id>", "zonas_show", zonas_inundables.show, methods=["POST"])
    app.add_url_rule("/zonas/delete/<zona_id>","zonas_delete",zonas_inundables.delete,methods=["POST"])
    app.add_url_rule("/zonas/update/<zona_id>", "zonas_update", zonas_inundables.update, methods=["POST"])
    app.add_url_rule("/zonas/editar/<zona_id>", "zonas_editar", zonas_inundables.new_update, methods=["POST"])
    app.add_url_rule("/zonas/pd/<zona_id>", "zonas_pd", zonas_inundables.pd, methods=["POST"])
    app.add_url_rule("/zonas/search", "zonas_search", zonas_inundables.search, methods=["POST"])

    # Rutas de Validacion y seguimiento
    app.add_url_rule("/validacion/<id>", "seguimiento_verDenuncia", seguimiento.verDenuncia, methods=["POST", "GET"])
    app.add_url_rule("/realizarLlamado/<id>", "seguimiento_realizarIntento", seguimiento.realizarIntento)
    app.add_url_rule("/realizarLlamadoExitoso/<id>", "seguimiento_IntentoExitoso", seguimiento.realizarIntentoExitoso)
    app.add_url_rule("/realizarSeguimiento/<id>", "seguimiento_create", seguimiento.realizar_seguimiento, methods=["POST"])
    app.add_url_rule("/resolverDenuncia/<id>", "seguimiento_resolverDenuncia", seguimiento.resolverDenuncia)
    app.add_url_rule("/reclamarDenuncia/<id>", "seguimiento_reclamarDenuncia", seguimiento.reclamarDenuncia)

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        return render_template("home.html")

    # Rutas de API-REST (usando Blueprints)
    api = Blueprint("api", __name__, url_prefix="/api")
    api.register_blueprint(zonaI_api)
    api.register_blueprint(denuncia_api)
    api.register_blueprint(recorridoE_api)
    api.register_blueprint(puntosE_api)
    api.register_blueprint(categorias_api)

    app.register_blueprint(api)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500

    # Retornar la instancia de app configurada
    return app
