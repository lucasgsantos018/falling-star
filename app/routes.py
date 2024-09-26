from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from werkzeug.utils import secure_filename
import os

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = current_user  # Use current_user para obter o usuário logado
    wishlists = [
        {
            'nome': {'nomeProduto': 'Esmaltes Risque'},
            'link': 'https://www.amazon.com.br/kit-Esmaltes-Risque-Cores-sortidas/dp/B07T3HP41M'
        },
        {
            'nome': {'nomeProduto': 'Semantic Error: Livro 1'},
            'link': 'https://www.amazon.com.br/Semantic-Error-Livro-1-J-Soori/dp/8583623368'
        }
    ]
    return render_template('user.html', title='Página Inicial', user=user, wishlists=wishlists)


#verificando usuário e senha para logar
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Entrar', form=form)

#deslogar
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#registrar usuários

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.set_avatar()
        db.session.add(user)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!')
        return redirect(url_for('login'))
    return render_template('cadastro.html', title='Cadastro', form=form)

#imagem de perfil
@app.route('/user')
@login_required
def user():
    user = current_user
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/criarLista', methods=['GET', 'POST'])
@login_required
def criarLista():
    user = current_user
    if request.method == 'POST':
        nome = request.form.get('nome')
        privacidade = request.form.get('privacidade')
        print(f'Nome da Lista: {nome}')
        print(f'Privacidade: {privacidade}')
        return redirect(url_for('index'))
    return render_template('criarLista.html')
    

# #editar perfil
# from app.forms import EditProfileForm

# Defina o caminho absoluto para o diretório de uploads
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

@app.route('/editarPerfil', methods=['GET', 'POST'])
def editarPerfil():
    user = current_user  # Pegando o usuário atual logado

    if request.method == 'POST':
        # Captura os dados do formulário
        nome_usuario = request.form.get('nome_usuario')
        email = request.form.get('email')
        senha = request.form.get('senha')
        foto_perfil = request.files.get('foto_perfil')

        # Verifica se os dados foram enviados e atualiza o objeto user
        if nome_usuario:
            user.nome_usuario = nome_usuario  # Atualiza o nome de usuário
        if email:
            user.email = email  # Atualiza o email
        if senha:
            user.set_password(senha)  # Certifique-se de que o método para definir a senha existe

        # Lida com o upload da foto de perfil, se enviada
        if foto_perfil and foto_perfil.filename != '':
            # Gera um nome seguro para o arquivo
            filename = secure_filename(foto_perfil.filename)
            
            # Define o caminho para salvar o arquivo
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            
            # Salva o arquivo na pasta uploads
            foto_perfil.save(file_path)
            
            # Atualiza o campo de foto do perfil do usuário no banco de dados
            user.foto_perfil_filename = filename
        else:
            # Se o arquivo não for permitido, pode adicionar uma mensagem de erro aqui
            print("Formato de arquivo não permitido!")

        # Persiste as mudanças no banco de dados
        db.session.commit()

        # Redireciona o usuário após a atualização
        return redirect(url_for('index'))

    return render_template('editarPerfil.html', user=user)