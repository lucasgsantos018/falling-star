from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from hashlib import md5
from flask import url_for

#criando a tabela usuário e seus atributos
class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    wishlist: so.Mapped[list['Wishlist']] = so.relationship(back_populates='author')

    def __repr__(self):
        return '<Usuário {}>'.format(self.username)
    
    #settando o password hashing
    #Com esses dois métodos implementados, um objeto de usuário agora é capaz de realizar a verificação segura de senhas, sem a necessidade de armazenar as senhas originais.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        if self.avatar:
            # Retorna a URL da imagem de perfil na pasta uploads
            return url_for('static', filename=f'uploads/{self.avatar}')
        else:
            # Se o usuário não tiver uma imagem de perfil, retorna uma imagem padrão
            return url_for('static', filename=f'uploads/default-profile.png')
    
#criando a tabela wishlist    
class Wishlist(db.Model):
    __tablename__ = 'wishlist'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(140))
    body: so.Mapped[str] = so.mapped_column(sa.String(500))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True), index=True, default=lambda: datetime.now(timezone.utc)
    )
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='wishlist')

    def __repr__(self):
        return '<Wishlist {}>'.format(self.title)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))