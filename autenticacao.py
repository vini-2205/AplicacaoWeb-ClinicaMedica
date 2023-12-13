from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user
from flask_login import login_required, login_user, current_user, logout_user
from bancoDeDados import connection


class Usuario(UserMixin):
    def __init__(self, user_id, email):
        self.id = user_id
        self.email = email

# # Renderizar página de login
# @app.route('/login')
# def index_login():
#     return render_template('./templates/login.html')

# # Verificar log
# @app.route('/login', methods=['POST'])

# def logar():
#     email = request.form['email']
#     senhahash = request.form['senhahash']

#     query = "SELECT * FROM FUNCIONARIO WHERE email = %s"
#     valores_usuario = (email)

#     cursor = connection.cursor(dictionary=True)
#     cursor.execute(query, valores_usuario)
#     user = cursor.fetchone()

#     if user and user['senhahash'] == senhahash:
#         usuario = Usuario(user['senhahash'], user['email'])
#         login_user(usuario)
#         return redirect(url_for('./templates/home-restrito.html'))
#     else:
#         # Autenticação falhou
#         return jsonify({'message': 'Email ou senha incorretos'}), 401

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))