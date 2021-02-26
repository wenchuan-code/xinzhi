# -*- coding: utf-8 -*-
"""
设置url
"""
from flask import Blueprint
from flask_restful import Api
from app.resources import test
from app.resources import auth

api_v1 = Blueprint('api_v1', __name__)
api = Api(api_v1)

api.add_resource(test.TestListResource, '/tests')
api.add_resource(test.TestResource, '/tests/<string:id>')

api.add_resource(auth.UserResource, '/auth/users', endpoint='users')
api.add_resource(auth.authLoginResource, '/auth/login')
api.add_resource(auth.authInfoResource, '/auth/info', endpoint='token')
api.add_resource(auth.TokenDataResource, '/auth/data')
