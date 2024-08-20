from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
import sqlalchemy as sa
from app import db
from flask import request
from urllib.parse import urlsplit
from app.forms import RegistrationForm

from app.models import User

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username':'Jessica'}
    wishlists = [
        {
            'nome': {'nomeProduto': 'Esmaltes Risque'},
            'link': 'https://www.amazon.com.br/kit-Esmaltes-Risque-Cores-sortidas/dp/B07T3HP41M/ref=sr_1_2?__mk_pt_BR=ÅMÅŽÕÑ&crid=164IBH8N736NP&dib=eyJ2IjoiMSJ9.LsHywaZE1d28v1sCgCogvJWEJI9E3pLW-ag6nCN_a7aWfLnFDR9tpRdMxLNCajdwNZnqqQlGkSx0aSAYdZHw33PWDjqzzzOf1cFbdfgSRCK5kGkAhx9tKKUIjKNynWkQbL378wKJ_tne4saGmIOQXnJZeG1Y1JlG-8zEz-JAXzTlYzAHLOSkLOZrIMyI0YGhmhlF2I-MFVPqiznxOYq8DXh1rcNew-08XoNk8kOZxwP_S7OM_eBJBdMIcqXaKH_wejJrD6Nb-5gWvq2gKz5tHuoHEh3X0DCmVr8AYDlbEGQ.dm3XAma9m4CdGhSb5juhSseGPPADBUVSVkrqdZavV6c&dib_tag=se&keywords=esmalte+risque+kit&qid=1724137293&sprefix=esmalte+risque+kit%2Caps%2C262&sr=8-2&ufe=app_do%3Aamzn1.fos.a492fd4a-f54d-4e8d-8c31-35e0a04ce61e'
        },
        {
            'nome': {'Semantic Error: Livro 1'},
            'link': 'https://www.amazon.com.br/Semantic-Error-Livro-1-J-Soori/dp/8583623368/ref=sr_1_2?__mk_pt_BR=ÅMÅŽÕÑ&crid=3IK5INPUD3AIZ&dib=eyJ2IjoiMSJ9.8Qo8bUreMhpXNBBMGNkMkD5_G1WJn3g2YKBrF2utcxvFbVXTHTgk9qgOjISNv6XcxPDik_ijI_vZ9d6EPFtEQr4mjy5eg3KqTHjIhHPzdTOnf60EkqZcAmn-DKabiU-5wWiCiOejysQ5jhBYVtFlcOAZs1cC-Rq4EJn4ALFlpTGLbbzXxcvNt5avsogqx7DMyCDngUfWLAvjPoz-Pm_WHzSsP6smUuh7H8z-AkSdiy7Pw_cDtZE2iAhA83YMfVScdG9qY6mOnaKRdgmS_gbqrZWxNBDvftm3X2sDphJO--E.Lb8e7WTIGp7K9OG9fgC1djyya5B634rc477Gd4OYUR0&dib_tag=se&keywords=semantic+error&qid=1724137350&sprefix=semantic+error%2Caps%2C218&sr=8-2!'
        }
    ]
    return render_template('index.html', title='Home Page', wishlists=wishlists)

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
            flash('Usuário ou senha incorreto')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

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
        flash('Usuário cadastrado com sucessp!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)