from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user
from flask_login import login_required, login_user, current_user, logout_user
#from PyPDF2 import PdfReader, PdfWriter
from werkzeug.utils import secure_filename
import os
from bancoDeDados import connection
from obter_localizacao import obter_localizacao
import os
#import pywhatkit as kt
import pyautogui as pg

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static\\arquivos\\candidato'
#app.config['SECRET_KEY'] = '123456'
#login_manager = LoginManager(app)



n=0


class Usuario(UserMixin):
    def __init__(self, user_id, email):
        self.id = user_id
        self.email = email


# Rota de GET para renderizar a página de cadastro
@app.route('/')
def index_cadastro():
    return render_template('Home.html')
        
# Renderizar página de reports
@app.route('/reports')
def index_reports():
      return render_template('reports.html')

# Obter informações do formulário de reports
@app.route('/reports', methods=['POST'])
def report():
      nome = request.form['nome']
      centro_custo = request.form['centro-custo']
      referencia = request.form['referencia']
      descricao = request.form['descricao']

      query = "INSERT INTO REPORTS (nome, centro_custo, referencia_atuacao, descricao) \
        VALUES (%s, %s, %s, %s)"
      
      values = (
            nome, centro_custo, referencia, descricao
      )

      # Obter localização
      localizacao = obter_localizacao()

      if localizacao is not None:
        query = "INSERT INTO REPORTS (nome, centro_custo, referencia_atuacao, descricao, \
                    pais, estado, cidade) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"
           
        cidade = localizacao['cidade']
        estado = localizacao['estado']
        pais = localizacao['pais']

        values = (
            nome, centro_custo, referencia, descricao, pais, estado, cidade
        )

      cursor = connection.cursor()
      cursor.execute(query, values)
      connection.commit()

      return index_reports()

# Renderizar página de login
@app.route('/login')
def index_login():
    return render_template('login.html')

# Verificar log
@app.route('/login', methods=['POST'])

def logar():
    email = request.form['email']
    senhahash = request.form['senhahash']

    query = "SELECT * FROM FUNCIONARIO WHERE email = %s"
    valores_usuario = (email,)

    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, valores_usuario)
    user = cursor.fetchone()

    if user and user['senhahash'] == senhahash:
        usuario = Usuario(user['senhahash'], user['email'])
        login_user(usuario)
        return redirect(url_for('portal_interno'))
    else:
        # Autenticação falhou
        return jsonify({'message': 'CPF ou senha incorretos'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Renderizando a página de registro
@app.route('/registrar-funcionario')
def index_registrarFuncionario():
     return render_template('registrar-funcionario.html')

# Registrar um usuário
@app.route('/registrar-funcionario', methods=['POST'])
def registrarFuncionario():
    email = request.form['email']
    senhahash = request.form['senhahash']

    consulta_proximo_codigo = "SELECT COALESCE(MAX(codigo), 0) + 1 AS proximo_codigo FROM FUNCIONARIO"
    query = "INSERT INTO FUNCIONARIO (email, senha, codigo) VALUES (%s, %s, %s)"
     
    cursor = connection.cursor()
    cursor.execute(consulta_proximo_codigo)
    proximo_codigo = cursor.fetchone()['proximo_codigo']
    valores_usuario = (email, senhahash, proximo_codigo)
    cursor.execute(query, valores_usuario)
    connection.commit()
    
    return index_login() # Redirecionando para o login


@app.route('/portal_interno')
@login_required
def portal_interno():
    # Acesso permitido apenas para usuários autenticados
    return render_template('portal_interno.html')


# Renderizando a página de registro
@app.route('/cadastrar-endereco')
def index_cadastrarEndereco():
     return render_template('cadastrar-endereco.html')

# Registrar um usuário
@app.route('/cadastrar-endereco', methods=['POST'])
def cadastrarEndereco():
    cep = request.form['cep']
    logradouro = request.form['logradouro']
    bairro = request.form['bairro']
    cidade = request.form['cidade']
    estado = request.form['estado']

    query = "INSERT INTO ENDERECOS (cep, logradouro, bairro, cidade, estado) VALUES (%s, %s, %s, %s, %s)"
     
    cursor = connection.cursor()
    valores_usuario = (cep, logradouro, bairro, cidade, estado)
    cursor.execute(query, valores_usuario)
    connection.commit()
    
    return index_cadastrarEndereco() # Redirecionando para o login

# Observar os candidatos cadastrados
@app.route('/visualizarCandidatos')
def verCandidato():
    cursor = connection.cursor()
    query = "SELECT cpf,nome,funcao,situacao FROM candidato"
    cursor.execute(query)
    candidatos = cursor.fetchall()
    return render_template('visualizarCandidatos.html',candidatos=candidatos)

# def atualizar_status_aprovado(cpf)://
@app.route('/visualizarCandidatos', methods=['POST'])
def index_post_visualizar():
    cpf = request.form['cpf']
    cursor = connection.cursor()
    sql = "UPDATE candidato SET situacao = 'Aprovado' WHERE cpf = %s"
    cursor.execute(sql, (cpf,))
    connection.commit()
    return verCandidato()

# Observar os reports cadastrados
@app.route('/visualizarReports')
def verReports():
    cursor = connection.cursor()
    query = "SELECT nome,centro_custo,referencia_atuacao,descricao FROM reports"
    cursor.execute(query)
    reports = cursor.fetchall()
    return render_template('visualizarReports.html',reports=reports)
    
# Renderizar o página de cadastro de area
@app.route('/cadastroArea')
def index_area():
        return render_template('cadastroAreas.html')

# Obter os valores do form da página de cadastro de área
@app.route('/cadastroArea', methods=['POST'])
def cadastrarArea():
    # Pasta que ficará os pdfs
    app.config['UPLOAD_FOLDER'] = 'static\\arquivos\\area'
    uploaded_files = request.files
    file_paths = {}

    for field_name, file in uploaded_files.items():
        # Verifica se o arquivo existe e se sua extensão é permitida
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Garante um nome de arquivo seguro
            file_path = os.path.join(filename)  # Constrói o caminho completo de destino

            file.save(file_path)  # Salva o arquivo no servidor
            file_paths[field_name] = file_path  # Armazena o caminho do arquivo no dicionário
            comprimir_pdf(file_path)

    #inserir na tabela area
    #--------------------------------------------------
    codigo = request.form['codigo']
    descricao = request.form['descricao']
    status = request.form['status']
    anexo = request.form.getlist('anexo')
    

    query = "INSERT INTO cadastroAE (codArea,descArea,statusLiberacao,caminho_anexo) VALUES (%s, %s, %s, %s)"

    values = (codigo,descricao,status,file_paths.get('anexo'))
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()

    # kt.sendwhatmsg_instantly("+5531984306223","Cadastro Realizado",15)

    return render_template('cadastroAreas.html')
    
    
# Renderizar o página de cadastro de area
@app.route('/solicitacoes')
def index_req():
        return render_template('solicitacoes.html')

@app.route('/solicitacoes', methods=['POST'])
def cadastrarReq():

    #inserir na tabela requisicao
    #--------------------------------------------------
    cpf_func = request.form['cpf']
    tipo = request.form['tipo-req']
    data = request.form['data']
    

    query = "INSERT INTO requisicoes (cpf_func,tipo,data_agen) VALUES (%s, %s,%s)"

    values = (cpf_func,tipo,data)
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()

    return index_req()

# Observar os candidatos cadastrados
@app.route('/visualizarRequisicoes')
def verRequisicoes():
    cursor = connection.cursor()
    query = "SELECT cpf_func,tipo,data_agen,status_req FROM requisicoes"
    cursor.execute(query)
    requisicoes = cursor.fetchall()
    return render_template('visualizarRequisicoes.html',requisicoes=requisicoes)
    

@app.route('/visualizarRequisicoes', methods=['POST'])
def index_Requisicoes():
    cpf = request.form['cpf']
    tipo = request.form['tipo']
    status = request.form['aprovar_func']
    cursor = connection.cursor()
    if tipo == 'Rescisao':
        opcao = request.form['opcao']
        avaliacao = request.form['avaliacao']
        sql = "UPDATE requisicoes SET status_req = %s,opcao = %s,avaliacao = %s WHERE cpf_func = %s"
        cursor.execute(sql, (status, opcao, avaliacao, cpf,))
    else :
        sql = "UPDATE requisicoes SET status_req = %s WHERE cpf_func = %s"
        cursor.execute(sql, (status,cpf,))

    connection.commit()
    return verRequisicoes()


# Observar os candidatos cadastrados
@app.route('/portalInterno/visualizarAreas')
def verAreas():
    cursor = connection.cursor()
    query = "SELECT * FROM cadastroAE"
    cursor.execute(query)
    areas = cursor.fetchall()
    return render_template('visualizarAreasEquipamentos.html',areas=areas)

@app.route('/visualizarAreas', methods=['POST'])
def verArea():
    cursor = connection.cursor()
    query = "SELECT * FROM cadastroAE"
    cursor.execute(query)
    areas = cursor.fetchall()
    return render_template('visualizarAreaEquipamento.html',areas=areas)
    

@app.route('/area/<codArea>')
def area(codArea):
    cursor = connection.cursor()
    query = "SELECT * FROM cadastroAE"
    cursor.execute(query)
    areas = cursor.fetchall()

    caminho_pdf = "file:///C:/Users/Pedro/OneDrive/Documents/Programming/HackathonItauna/HackathonItauna"
    
    area_data = None
    for area in areas:
        if area[0] == codArea:  # Assumindo que o primeiro campo é o codArea
            area_data = {
                "codArea": area[0],
                "descArea": area[1],
                "statusLiberacao": area[2],
                "caminho_anexo": caminho_pdf + "/" + area[3]
            }
            break
    
    if area_data:
        pdf_path = os.path.join(app.static_folder, "pdfs", area_data["caminho_anexo"])
        return render_template('paginaAreaEquipamento.html', area=area_data, pdf_path=pdf_path)
    else:
        return "Área não encontrada!"

        
@app.route('/portalInterno')
def index_portal_interno():
    return render_template('portalInterno.html')
