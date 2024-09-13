from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

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
        db.session.add(user)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!')
        return redirect(url_for('login'))
    return render_template('cadastro.html', title='Register', form=form)

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

#criar lista
@app.route('/criarLista')
@login_required
def criarLista():
    user = current_user
    

# #editar perfil
# from app.forms import EditProfileForm

# @app.route('/edit_profile', methods=['GET', 'POST'])
# @login_required
# def edit_profile():
#     form = EditProfileForm()
#     if form.validate_on_submit():
#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         current_user.password = form.password.data
#         db.session.commit()
#         flash('Alterações Salvas!')
#         return redirect(url_for('edit_profile'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user.email
#         form.password.data = current_user.password
#     return render_template('edit_profile.html', title='Editar Perfil',
#                            form=form)