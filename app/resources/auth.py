"""

    使用-Flask-设计-RESTful-的认证-—-Designing-a-RESTful-API-with-Python-and-Flask-1.0-documentation    \
    http://www.pythondoc.com/flask-restful/third.html

    Flask 使用类似的方式处理 cookies 的。这个实现依赖于一个叫做 itsdangerous 的库，我们这里也会采用它。


    用户注册  curl -i -X POST -H "Content-Type: application/json" -d '{"username":"chilly","password":"python"}' http://127.0.0.1:5000/api/v1/auth/users
    用户名和密码获取  curl -i -X POST -H "Content-Type: application/json" -d '{"username":"chilly","password":"python"}' http://127.0.0.1:5000/api/users
        获取token  curl -u chilly:python -i -X GET http://127.0.0.1:5000/api/token
    token验证获取 curl -u eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZXhwIjoxNjE0MTM2MDUzLjc2NzM4Mzh9.btgBzalHtmu9KepUrGIVJvS1RULI4HTs_92z5ts-Z3s:unused -i -X GET http://127.0.0.1:5000/api/resource

"""

from flask import g, url_for, jsonify, redirect
from app.models.user import User
from app.models import db
from app.common import auth
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from app.common import pretty_result, code, verify_password


class UserResource(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def post(self):
        """
        用户注册
        :return: 用户名
        """
        self.parser.add_argument("username", type=str, location="json", required=True)
        self.parser.add_argument("password", type=str, location="json", required=True)
        args = self.parser.parse_args()

        username = args.username
        password = args.password
        if username is None or password is None:
            return pretty_result(code.PARAM_ERROR)  # missing arguments
        if User.query.filter_by(username=username).first() is not None:
            return pretty_result(code.PARAM_ERROR)  # existing user
        user = User(username=username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return pretty_result(code.OK, data={'username': user.username})


class authLoginResource(Resource):
    """
    用户验证登录
    """
    def __init__(self):
        self.parser = RequestParser()

    def post(self):

        self.parser.add_argument("username", type=str, location="json", required=True)
        self.parser.add_argument("password", type=str, location="json", required=True)
        args = self.parser.parse_args()

        username = args.username
        password = args.password
        if username is None or password is None:
            return pretty_result(code.PARAM_ERROR)  # missing arguments
        if verify_password(username, password) is True:
            # 账号和密码验证正确，返回token
            # return (jsonify({'username': ''}), 201,{'Location': url_for(TokenAuthResource, _external=True)})
            token = g.user.generate_auth_token(600)
            return pretty_result(code.OK, data={'token': token, 'duration': 600})
        else:
            return pretty_result(code.PARAM_ERROR)


class authInfoResource(Resource):

    def __init__(self):
        self.parser = RequestParser()

    # @auth.login_required
    def get(self):
        """获取用户信息

            Add some data in this routing

            Args:
                token

            Returns:
                用户信息
            """

        self.parser.add_argument("token", type=str, location="args")
        args = self.parser.parse_args()

        # 解码token得到用户名并查询用户信息
        if verify_password(args.token, '') is True:
            user = g.user
            info = {
                'id':user.id,
                'username':user.username
            }
            return pretty_result(code.OK, data=info)
        else:
            return pretty_result(code.PARAM_ERROR, data=args.token)



class TokenDataResource(Resource):
    def __init__(self):
        self.parser = RequestParser()

    # @auth.login_required
    def get(self):
        """获取用户信息

            Add some data in this routing

            Args:
                pass

            Returns:
                pass
            """
        return g.user.username
        # self.parser.add_argument("token", type=str, location="args")
        # args = self.parser.parse_args()
        #
        # token = args.token
        # return pretty_result(code.Ok, data={'data': 'Hello, %s!' % g.user.username})



