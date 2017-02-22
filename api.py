#  Python Packages
from flask import Flask
from flask_restful import Resource, Api

# Custom Packages
import api_constants

app = Flask(__name__)
api = Api(app)

class ServerInformation(Resource):
    def get(self):
        return api_constants.API_INFORMATION

api.add_resource(ServerInformation, '/')


if __name__ == '__main__':
    app.run(debug=True)
