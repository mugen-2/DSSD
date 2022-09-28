from flask import render_template, request
from flask.json import jsonify


def not_found_error(e):
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La url a la que quiere acceder no existe",
    }
    if request.path.startswith("/api/"):
        kwargs["error_description"]="El recurso al que quiere acceder no existe"
        return jsonify(kwargs), 404
    else:
        return render_template("error.html", **kwargs), 404


def unauthorized_error(e):
    kwargs = {
        "error_name": "401 Unauthorized Error",
        "error_description": "No está autorizado para acceder a la url",
    }
    return render_template("error.html", **kwargs), 401
