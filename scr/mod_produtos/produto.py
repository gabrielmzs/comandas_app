from flask import Blueprint, render_template
import requests
from mod_login.login import validaToken
from settings import getHeadersAPI, ENDPOINT_PRODUTO
bp_produto = Blueprint('produto', __name__, url_prefix="/produto", template_folder='templates')

''' rotas dos formulários '''
@bp_produto.route('/', methods=['GET', 'POST'])
@validaToken
def formListaProduto():
    try:
        response = requests.get(ENDPOINT_PRODUTO,headers=getHeadersAPI())
        result = response.json()

        print(result) # para teste
        print(response.status_code) # para teste

        if (response.status_code != 200):
            raise Exception(result)
        
        return render_template('formListaProduto.html', result=result[0])
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])

@bp_produto.route('/form-produto/')
@validaToken
def formProduto():
    return render_template('formProduto.html')