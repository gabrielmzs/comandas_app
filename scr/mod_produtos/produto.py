from flask import Blueprint, redirect, render_template, request, jsonify, url_for, make_response
import requests
import base64
from mod_login.login import validaToken
from settings import ENDPOINT_PRODUTO, getHeadersAPI
from xhtml2pdf import pisa
import io

bp_produto = Blueprint('produto', __name__, url_prefix="/produto", template_folder='templates')

@bp_produto.route('/', methods=['GET', 'POST'])
def formListaProduto():
    try:
        response = requests.get(ENDPOINT_PRODUTO, headers=getHeadersAPI())
        result = response.json()
        
        if response.status_code != 200:    
            raise Exception(result)
        
        return render_template('formListaProduto.html', result=result[0])
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])

@bp_produto.route('/form-produto/')
@validaToken
def formProduto():
    return render_template('formProduto.html')

@bp_produto.route("/form-edit-produto", methods=['POST'])
@validaToken
def formEditProduto():
    try:
        id_produto = request.form['id']

        response = requests.get(f"{ENDPOINT_PRODUTO}{id_produto}", headers=getHeadersAPI())
        result = response.json()
        
        if response.status_code != 200:
            raise Exception(result)
        
        return render_template('formProduto.html', result=result)
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])

@bp_produto.route('/insert', methods=['POST'])
def insert():
    try:
        id_produto = 0
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor = request.form['valor']
        foto = "data:" + request.files['foto'].content_type + ";base64," + str(base64.b64encode(request.files['foto'].read()), "utf-8")
        
        payload = {
            'id_produto': id_produto,
            'nome': nome,
            'descricao': descricao,
            'foto': foto,
            'valor': valor
        }
        
        response = requests.post(ENDPOINT_PRODUTO, headers=getHeadersAPI(), json=payload)
        result = response.json()
        
        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)
        
        return redirect(url_for('produto.formListaProduto', msg=result[0]))
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])

@bp_produto.route('/edit', methods=['POST'])
@validaToken
def edit():
    try:
        id_produto = request.form['id']
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor = request.form['valor']
        foto = "data:" + request.files['foto'].content_type + ";base64," + str(base64.b64encode(request.files['foto'].read()), "utf-8")
        
        payload = {
            'id_produto': id_produto,
            'nome': nome,
            'descricao': descricao,
            'foto': foto,
            'valor': valor
        }
        
        response = requests.put(f"{ENDPOINT_PRODUTO}{id_produto}", headers=getHeadersAPI(), json=payload)
        result = response.json()
        
        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)
        
        return redirect(url_for('produto.formListaProduto', msg=result[0]))
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])

@bp_produto.route('/delete', methods=['POST'])
@validaToken
def delete():
    try:
        id_produto = request.form['id_produto']
        
        response = requests.delete(f"{ENDPOINT_PRODUTO}{id_produto}", headers=getHeadersAPI())
        result = response.json()
        
        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)
        
        return jsonify(erro=False, msg=result[0])
    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])

@bp_produto.route('/generate-pdf', methods=['GET'])
@validaToken
def generate_pdf():
    try:
        response = requests.get(ENDPOINT_PRODUTO, headers=getHeadersAPI())
        result = response.json()

        if response.status_code != 200:
            raise Exception(result)
        
        html = render_template('produtos_pdf.html', result=result[0])
        pdf = io.BytesIO()
        pisa.CreatePDF(io.BytesIO(html.encode('UTF-8')), dest=pdf)
        pdf.seek(0)
        return make_response(pdf.getvalue(), 200, {'Content-Type': 'application/pdf', 'Content-Disposition': 'attachment; filename=produtos.pdf'})
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])

        
        