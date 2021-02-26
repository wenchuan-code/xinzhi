# -*- coding: utf-8 -*-
from . import db
from .base import BaseModel
import jwt
import time
from werkzeug.security import generate_password_hash, check_password_hash
from config import config


class User(db.Model, BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=600):
        '''
        获取token
        :param expires_in:
        :return:
        '''
        return jwt.encode(
            {'id': self.id, 'exp': time.time() + expires_in},
            config.SECRET_KEY, algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        '''
        根据token获得用户id
        :param token:
        :return:
        '''
        try:
            data = jwt.decode(token, config.SECRET_KEY,
                              algorithms=['HS256'])
        except:
            return
        return User.query.get(data['id'])