# -*- coding: utf-8 -*-
from flask import current_app, abort
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from app import hash_ids
from app.models import db
from app.common import code, pretty_result
from app.models.test import TestsModel
from flask import abort


class TestListResource(Resource):
    """
    示例test list资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        """Add some data

            Add some data in this routing

            Args:
                pass

            Returns:
                pass
            """

        self.parser.add_argument("page_num", type=int, location="args", default=1)
        self.parser.add_argument("page_size", type=int, location="args", default=10)
        args = self.parser.parse_args()

        try:
            tests = TestsModel.query.paginate(args.page_num, args.page_size, error_out=False)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, '数据库错误！')
        else:
            items = []
            for i in tests.items:
                items.append(
                    {
                        'id': hash_ids.encode(i.id),
                        'nickname': i.nickname,
                        'signature': i.signature
                    }
                )
            data = {
                'page_num': args.page_num,
                'page_size': args.page_size,
                'total': tests.total,
                'items': items
            }
            return pretty_result(code.OK, data=data)

    def post(self):
        """Add some data

            Add some data in this routing

            Args:
                pass

            Returns:
                pass
            """
        self.parser.add_argument("nickname", type=str, location="json", required=True)
        self.parser.add_argument("signature", type=str, location="json", required=True)
        args = self.parser.parse_args()

        test = TestsModel(nickname=args.nickname, signature=args.signature)

        try:
            db.session.add(test)
            db.session.commit()
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, '数据库错误！')
        else:
            return pretty_result(code.OK)


class TestResource(Resource):
    """
    示例test资源类
    """

    def __init__(self):
        self.parser = RequestParser()

    @staticmethod
    def get(id):
        """Add some data

            Add some data in this routing

            Args:
                pass

            Returns:
                pass
            """
        id = hash_ids.decode(id)
        if not id: abort(404)

        try:
            test = TestsModel.query.get(id[0])
            if not test: abort(404)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, '数据库错误！')
        else:
            item = {
                'id': hash_ids.encode(test.id),
                'nickname': test.nickname,
                'signature': test.signature
            }
            return pretty_result(code.OK, data=item)

    def put(self, id):
        self.parser.add_argument("nickname", type=str, location="json", required=True)
        self.parser.add_argument("signature", type=str, location="json", required=True)
        args = self.parser.parse_args()

        id = hash_ids.decode(id)
        if not id: abort(404)

        try:
            test = TestsModel.query.get(id[0])
            if not test: abort(404)

            test.nickname = args.nickname
            test.signature = args.signature

            db.session.add(test)
            db.session.commit()
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, '数据库错误！')
        else:
            return pretty_result(code.OK)

    @staticmethod
    def delete(id):
        id = hash_ids.decode(id)
        if not id: abort(404)

        try:
            test = TestsModel.query.get(id[0])
            if not test: abort(404)

            db.session.delete(test)
            db.session.commit()
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, '数据库错误！')
        else:
            return pretty_result(code.OK)


