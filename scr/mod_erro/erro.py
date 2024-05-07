from flask import Blueprint, render_template

bp_erro = Blueprint('erro', __name__, template_folder='templates')

@bp_erro.app_errorhandler(404)
def erro404(error):
    return render_template("form404.html", erroHttp=error)

@bp_erro.app_errorhandler(401)
def erro500(error):
    return render_template("form401.html", erroHttp=error)