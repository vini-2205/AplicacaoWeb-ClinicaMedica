from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, login_user, current_user, logout_user
#from PyPDF2 import PdfReader, PdfWriter
from werkzeug.utils import secure_filename
import os
from bancoDeDados import connection
from obter_localizacao import obter_localizacao
#import pywhatkit as kt
import pyautogui as pg

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static\\arquivos\\candidato'
app.config['SECRET_KEY'] = '123456'
login_manager = LoginManager(app)
login_manager.init_app(app)


n=0


class Usuario(UserMixin):
    def __init__(self, user_id, email):
        self.id = user_id
        self.email = email

# Rota de GET para renderizar a página de cadastro
@app.route('/')
def index_home():
    return render_template('Home.html')

@app.route('/galeria')
def index_galeria():
    return render_template('galeria.html')
        


# Renderizando a página de registro
@app.route('/cadastrar-funcionario')
@login_required
def index_cadastrarFuncionario():
     return render_template('cadastrar-funcionario.html')

# Registrar um usuário
@app.route('/cadastrar-funcionario', methods=['POST'])
@login_required
def cadastrarFuncionario():
    email = request.form['email']
    senhahash = request.form['senha']
    cep = request.form['cep']
    logradouro = request.form['logradouro']
    bairro = request.form['bairro']
    cidade = request.form['cidade']
    estado = request.form['estado']
    contrato = request.form['contrato']
    salario = request.form['salario']
    funcionario = request.form['funcionario']
    telefone = request.form['telefone']
    especialidade = None
    crm = None

    if 'especialidade' in request.form:
        especialidade = request.form['especialidade']
        crm = request.form['crm']

    consulta_proximo_codigo = "SELECT COALESCE(MAX(codigo), 0) + 1 AS proximo_codigo FROM FUNCIONARIO"
    query = "INSERT INTO FUNCIONARIO (email, senhahash, codigo, cep, logradouro, bairro, cidade, estado, datacontrato, salario, nomeCompleto, telefone,especialidade, crm) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s, %s,%s,%s)"
    
     
    cursor = connection.cursor()
    cursor.execute(consulta_proximo_codigo)
    proximo_codigo = cursor.fetchone()[0]
    print('Proximo codigo: ', proximo_codigo)
    valores_usuario = (email, senhahash, proximo_codigo, cep, logradouro, bairro, cidade, estado, contrato, salario, funcionario, telefone,especialidade, crm)
    cursor.execute(query, valores_usuario)

    connection.commit()
    
    return index_login() # Redirecionando para o login


# Renderizando a página de registro
@app.route('/cadastrar-paciente')
@login_required
def index_cadastrarPaciente():
     return render_template('cadastrar-paciente.html')

# Registrar um usuário
@app.route('/cadastrar-paciente', methods=['POST'])
@login_required
def cadastrarPaciente():
    paciente = request.form['paciente']
    email = request.form['email']
    telefone = request.form['telefone']
    cep = request.form['cep']
    logradouro = request.form['logradouro']
    bairro = request.form['bairro']
    cidade = request.form['cidade']
    estado = request.form['estado']
    peso = request.form['peso']
    altura = request.form['altura']
    tipoSanguineo = request.form['tipoSanguineo']

    consulta_proximo_codigo = "SELECT COALESCE(MAX(codigo), 0) + 1 AS proximo_codigo FROM PACIENTE"
    query = "INSERT INTO PACIENTE (email, telefone, codigo, cep, logradouro, bairro, cidade, estado, peso, altura, nomeCompleto, tipoSanguineo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s, %s)"
    
     
    cursor = connection.cursor()
    cursor.execute(consulta_proximo_codigo)
    proximo_codigo = cursor.fetchone()[0]
    print('Proximo codigo: ', proximo_codigo)
    valores_usuario = (email, telefone, proximo_codigo, cep, logradouro, bairro, cidade, estado, peso, altura, paciente, tipoSanguineo)
    cursor.execute(query, valores_usuario)

    connection.commit()
    
    return redirect(url_for(index_home))

# Rota para a API que retorna os dados do CEP
@app.route('/api/busca_cep', methods=['POST'])
def busca_cep():
    cep_digitado = request.json['cep']
    # Conecta ao banco de dados MySQ
    cursor = connection.cursor()
    query2 = "SELECT * FROM ENDERECOS WHERE cep = (%s)"
    valores_usuario2 = (cep_digitado,)
    cursor.execute(query2, valores_usuario2)    
    cep_encontrado = cursor.fetchone()


    if cep_encontrado:
        # Se o CEP for encontrado, retorna os dados em formato JSON
        return jsonify({
            'success': True,
            'cep': cep_encontrado[0],
            'bairro': cep_encontrado[2],
            'logradouro': cep_encontrado[1],
            'cidade': cep_encontrado[3],
            'estado': cep_encontrado[4]
        })
    else:
        # Se o CEP não for encontrado, retorna uma mensagem de erro
        print("Entrou false")  # Apenas para debug
        return jsonify({'success': False, 'message': 'CEP não encontrado'})
    
    
@app.route('/api/busca_medicos', methods=['POST'])
def busca_medicos():
    especialidade = request.json['especialidade']
    # Conecta ao banco de dados MySQ
    cursor = connection.cursor()
    query2 = "SELECT nomeCompleto FROM FUNCIONARIO WHERE especialidade = (%s)"
    valores_usuario2 = (especialidade,)
    cursor.execute(query2, valores_usuario2)    
    medicos = cursor.fetchall()


    if medicos:
        # Retorna os nomes dos médicos em formato JSON
        nomes_medicos = [medico[0] for medico in medicos]
        return jsonify({
            'success': True,
            'medicos': nomes_medicos
        })
    else:
        return jsonify({
            'success': False,
            'medicos': []
        })

@app.route('/api/busca_horario', methods=['POST'])
def busca_horario():
    medico = request.json['medico']
    data = request.json['data']
    horariosTotais = [8,9,10,11,12,13,14,15,16,17]

    # Conecta ao banco de dados MySQ
    cursor = connection.cursor()
    query = "SELECT codigo FROM FUNCIONARIO WHERE nomeCompleto = (%s)"
    value = (medico,)
    cursor.execute(query, value)
    codigo = cursor.fetchone()[0]


    query2 = "SELECT horario FROM HorariosDisponiveis WHERE data = (%s) and codMedico = (%s)"
    valores_usuario2 = (data, codigo,)
    cursor.execute(query2, valores_usuario2)    
    horarios = cursor.fetchall()
    horariosOcupados = [horariosTotais[0] for horariosTotais in horarios]
    set_horarios_Totais = set(horariosTotais)
    set_horarios_ocupados = set(horariosOcupados)
    horarios_disponiveis_final = set_horarios_Totais - set_horarios_ocupados

    horarios_disponiveis_final_lista = list(horarios_disponiveis_final)


    if horarios_disponiveis_final_lista:

        return jsonify({
            'success': True,
            'horarios': horarios_disponiveis_final_lista
        })
    else:
        return jsonify({
            'success': False,
            'horarios': []
        })

# Renderizando a página de registro
@app.route('/agendar-consulta')
def index_agendarConsulta():
    consulta_especialidade = "SELECT DISTINCT especialidade FROM FUNCIONARIO WHERE especialidade IS NOT NULL AND especialidade <> ''"
    
    # Conecta ao banco de dados MySQL
    cursor = connection.cursor()
    cursor.execute(consulta_especialidade)    
    especialidades = [especialidade[0] for especialidade in cursor.fetchall()]
    return render_template('agendar-consulta.html', especialidades=especialidades)

# Registrar um usuário
@app.route('/agendar-consulta', methods=['POST'])
def agendarConsulta():
    data = request.form['data']
    horario = request.form['horario']
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    medico = request.form['medico']

    cursor = connection.cursor()

    # Obtendo o código do médico
    query_codigo_medico = "SELECT codigo FROM FUNCIONARIO WHERE nomeCompleto = (%s)"
    valores_codigo_medico = (medico,)
    cursor.execute(query_codigo_medico, valores_codigo_medico)
    codigoMedico = cursor.fetchone()[0]

    # Obtendo o próximo código para a tabela AGENDA
    consulta_proximo_codigo = "SELECT COALESCE(MAX(codigo), 0) + 1 AS proximo_codigo FROM AGENDA WHERE codigomedico = (%s)"
    valores_proximo_codigo = (codigoMedico,)
    cursor.execute(consulta_proximo_codigo, valores_proximo_codigo)
    proximo_codigo = cursor.fetchone()[0]

    # Inserindo na tabela AGENDA
    query_agenda = "INSERT INTO AGENDA (email, telefone, codigo, codigomedico, data, horario, nome) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    valores_agenda = (email, telefone, proximo_codigo, codigoMedico, data, horario, nome)
    cursor.execute(query_agenda, valores_agenda)

    # Inserindo na tabela HorariosDisponiveis
    query_horarios_disponiveis = "INSERT INTO HorariosDisponiveis (data, horario, codMedico) VALUES (%s, %s, %s)"
    valores_horarios_disponiveis = (data, horario, codigoMedico)
    cursor.execute(query_horarios_disponiveis, valores_horarios_disponiveis)

    # Commitando as alterações no banco de dados
    connection.commit()

    # Redirecionando para o login
    return index_login()




@app.route('/cadastrar-prontuario')
@login_required
def index_cadastrarProntuario():
    consulta_pacientes = "SELECT nomeCompleto FROM PACIENTE"
    # Conecta ao banco de dados MySQL
    cursor = connection.cursor()
    cursor.execute(consulta_pacientes)
    pacientes = [paciente[0] for paciente in cursor.fetchall()]
    print(pacientes)
    return render_template('cadastrar-prontuario.html', pacientes=pacientes)

# Registrar um usuário
@app.route('/cadastrar-prontuario', methods=['POST'])
@login_required
def cadastrarProntuario():
    paciente = request.form['paciente']
    anamnese = request.form['anamnese']
    medicamentos = request.form['medicamentos']
    atestado = request.form['atestado']
    exame = request.form['exame']

    cursor = connection.cursor()

    # Obtendo o código do médico
    query_codigo_paciente = "SELECT codigo FROM PACIENTE WHERE nomeCompleto = (%s)"
    valores_codigo_paciente = (paciente,)
    cursor.execute(query_codigo_paciente, valores_codigo_paciente)
    codigoPaciente = cursor.fetchone()[0]

    # Inserindo na tabela PRONTUARIO
    query_prontuario = "INSERT INTO PRONTUARIO (codigopaciente, anamnese, medicamentos, atestados, exames) VALUES (%s, %s, %s, %s, %s)"
    valores_prontuario = (codigoPaciente, anamnese, medicamentos, atestado, exame)
    cursor.execute(query_prontuario, valores_prontuario)

    # Commitando as alterações no banco de dados
    connection.commit()

    # Redirecionando para o login
    return index_login()


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

@app.route('/listar-funcionarios')
@login_required
def listarFuncionarios():
    cursor = connection.cursor()
    #query = "SELECT funcionario,email,crm,especialidade,telefone,cep,contrato,salario FROM FUNCIONARIO"
    query = "SELECT * FROM FUNCIONARIO"
    cursor.execute(query)
    funcionarios = cursor.fetchall()
    return render_template('listar-funcionarios.html',funcionarios=funcionarios)


@app.route('/listagem')
@login_required
def listagem():
    return render_template('listagem.html')

@app.route('/listar-pacientes')
@login_required
def listarPacientes():
    cursor = connection.cursor()
    query = "SELECT * FROM PACIENTE"
    cursor.execute(query)
    pacientes = cursor.fetchall()
    return render_template('listar-pacientes.html',pacientes=pacientes)

@app.route('/listar-enderecos')
@login_required
def listarEnderecos():
    cursor = connection.cursor()
    query = "SELECT * FROM ENDERECOS"
    cursor.execute(query)
    enderecos = cursor.fetchall()

    return render_template('listar-enderecos.html',enderecos=enderecos)

@app.route('/listar-agendamentos')
def listarAgendamento():
    cursor = connection.cursor()
    query = "SELECT * FROM AGENDA"
    cursor.execute(query)
    agendamentos = cursor.fetchall()

    return render_template('listar-agendamentos.html',agendamentos=agendamentos)

@app.route('/listar-agendamento-funcionario')
@login_required
def listarAgendamentoFuncionario():
    cursor = connection.cursor()
    codigo = current_user.id
    query = "SELECT crm FROM FUNCIONARIO WHERE codigo = %s"
    valores = (codigo,)
    cursor.execute(query,valores)
    crm = cursor.fetchone()
    
    if crm:
        query = "SELECT * FROM AGENDA WHERE codigomedico = %s"
        valores = (codigo,)
        cursor.execute(query,valores)
        agendamentos = cursor.fetchall()

    return render_template('listar-agendamentos.html',agendamentos=agendamentos)

@login_manager.user_loader
def load_user(user_id):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM FUNCIONARIO WHERE codigo = %s", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        user = Usuario(user_id=user_data['codigo'], email=user_data['email'])
        return user
    else:
        return None

# Renderizar página de login
@app.route('/login')
def index_login():
    return render_template('login.html')

# Verificar log
@app.route('/login', methods=['POST'])
def logar():
    email = request.form['email']
    senhahash = request.form['senhahash']

    query = "SELECT codigo FROM FUNCIONARIO WHERE email = %s and senhahash = %s"
    valores_usuario = (email, senhahash)

    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, valores_usuario)
    user = cursor.fetchone()

    if user:
        usuario = Usuario(user['codigo'], email)
        login_user(usuario)
        return redirect(url_for('index_home'))  
    else:
        return jsonify({'message': 'Email ou senha incorretos'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index_home')) 

