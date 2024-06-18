from flask import Blueprint, render_template, request, redirect, url_for, jsonify, make_response
import requests
from funcoes import Funcoes
from mod_login.login import validaToken
from settings import getHeadersAPI, ENDPOINT_CLIENTE
from xhtml2pdf import pisa
import io

bp_cliente = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')

''' rotas dos formulários '''
@bp_cliente.route('/', methods=['GET', 'POST'])
@validaToken
def formListaCliente():
    try:
        response = requests.get(ENDPOINT_CLIENTE, headers=getHeadersAPI())
        result = response.json()

        print(result)  # para teste
        print(response.status_code)  # para teste

        if response.status_code != 200:
            raise Exception(result)

        return render_template('formListaCliente.html', result=result[0])
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/form-cliente/')
@validaToken
def formCliente():
    return render_template('formCliente.html')

@bp_cliente.route('/insert', methods=['POST'])
def insert():
    try:
        # dados enviados via FORM
        id_cliente = request.form['id']
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']

        # monta o JSON para envio a API
        payload = {'id_cliente': id_cliente, 'nome': nome, 'cpf': cpf, 'telefone': telefone}
        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_CLIENTE, headers=getHeadersAPI(), json=payload)
        result = response.json()
        print(result)  # [{'msg': 'Cadastrado com sucesso!', 'id': 13}, 200]
        print(response.status_code)  # 200
        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)
        return redirect(url_for('cliente.formListaCliente', msg=result[0]))
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route("/form-edit-cliente", methods=['POST'])
def formEditCliente():
    try:
        id_cliente = request.form['id']

        response = requests.get(f"{ENDPOINT_CLIENTE}{id_cliente}", headers=getHeadersAPI())
        result = response.json()

        if response.status_code != 200:
            raise Exception(result)

        return render_template('formCliente.html', result=result[0])

    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/edit', methods=['POST'])
def edit():
    try:
        id_cliente = request.form['id']
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']

        payload = {
            'id_cliente': id_cliente,
            'nome': nome,
            'cpf': cpf,
            'telefone': telefone
        }

        response = requests.put(f"{ENDPOINT_CLIENTE}{id_cliente}", headers=getHeadersAPI(), json=payload)
        result = response.json()

        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)

        return redirect(url_for('cliente.formListaCliente', msg=result[0]))

    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/delete', methods=['POST'])
def delete():
    try:
        id_cliente = request.form['id']

        response = requests.delete(f"{ENDPOINT_CLIENTE}{id_cliente}", headers=getHeadersAPI())
        result = response.json()

        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)

        return jsonify(erro=False, msg=result[0])

    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])

@bp_cliente.route('/gerar_pdf', methods=['GET'])
@validaToken
def gerar_pdf():
    try:
        response = requests.get(ENDPOINT_CLIENTE, headers=getHeadersAPI())
        result = response.json()

        if response.status_code != 200:
            raise Exception(result)

        html = render_template('clientes_pdf.html', result=result[0])
        pdf = io.BytesIO()
        pisa.CreatePDF(io.BytesIO(html.encode('UTF-8')), dest=pdf)
        pdf.seek(0)
        return make_response(pdf.getvalue(), 200, {'Content-Type': 'application/pdf', 'Content-Disposition': 'attachment; filename=clientes.pdf'})
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])
