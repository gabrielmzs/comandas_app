from flask import Flask, render_template, request, session
from datetime import timedelta
from settings import HOST, PORT, DEBUG, TEMPO_SESSION

from mod_funcionario.funcionario import bp_funcionario
from mod_produtos.produto import bp_produto
from mod_clientes.cliente import bp_cliente
from mod_index.index import bp_index
from mod_login.login import bp_login
from mod_erro.erro import bp_erro
from utilities import is_active
import requests

import os
app = Flask(__name__)

@app.context_processor
def context_processor():
    return dict(is_active=is_active)

# gerando uma chave randômica para secret_key
app.secret_key = os.urandom(12).hex()

app.register_blueprint(bp_funcionario)
app.register_blueprint(bp_produto)
app.register_blueprint(bp_cliente)
app.register_blueprint(bp_index)
app.register_blueprint(bp_login)
app.register_blueprint(bp_erro)

app.config.update(
SESSION_COOKIE_SAMESITE='None',
SESSION_COOKIE_SECURE='True'
)

if __name__ == "__main__":
    """ Inicia o aplicativo WEB Flask """
    app.run(host=HOST, port=PORT, debug=DEBUG)

# método para renovar o tempo da sessão
@app.before_request
def before_request():
    session.permanent = True
    session['tempo'] = int(TEMPO_SESSION)
    # o padrão é 31 dias...
    app.permanent_session_lifetime = timedelta(minutes=session['tempo'])