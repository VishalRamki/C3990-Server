from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

API_INFORMATION = {
    "VERSION": "v0.1",
    "APPLICATION": "RethinkBeacon"
}

class ServerInformation(Resource):

    ## HTTP GET METHOD
    def get(self):
        return API_INFORMATION
