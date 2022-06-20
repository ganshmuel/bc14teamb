#!/usr/bin/env python3

from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)


def non_empty_string(s):
    if not s:
        raise ValueError("Must not be empty string")
    return s


parser = reqparse.RequestParser()
parser.add_argument('name', required=True, nullable=False, type=non_empty_string)


class ProviderPost(Resource):
    def post(self):
        args = parser.parse_args()
        name = {'name': args['name']}
        return name


class ProviderPut(Resource):
    def put(self, provider_id):
        args = parser.parse_args()
        args = parser.parse_args()
        name = {'name': args['name']}
        return name


api.add_resource(ProviderPost, '/', '/provider')
api.add_resource(ProviderPut, '/', '/provider/<string:provider_id>')

if __name__ == '__main__':
    print("Starting the job listing API")
    app.run(host="0.0.0.0", port=5000)
