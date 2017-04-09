from flask import Flask, send_file
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys, werkzeug, os

## Customer Helper Functions
from functions import *


class getmaterials(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(getmaterials, self).__init__()

    ## HTTP GET METHOD
    def get(self, id):
        pathTo = os.path.join("uploaded/", id)
        return send_file(pathTo)
        pass

    ## HTTP DELETE METHOD
    def delete(self):
        pass

    ## HTTP PUT METHOD
    def put(self):
        pass

    ## HTTP POST METHOD
    def post(self):
        pass
