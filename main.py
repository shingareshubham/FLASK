from flask import Flask
from flask_restful import Api, Resource

APP = Flask(__name__)
API = Api(APP)


class ProcessPayment(Resource):
    def get(self):
        return {'status':'OK'}


API.add_resource(ProcessPayment, '/v1/')

if __name__ == "__main__":
    APP.run(debug=True)