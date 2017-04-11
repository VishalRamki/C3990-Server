##
##  getmaterials.py
##
##  provides the beacon endpoint;
##
##  ENDPOINT: /api/materials/<string:id>
##  REST STATES: GET
##
##  Input:
##  id - found in the URL of the request.
##
##
##  Example: GET
##  curl -X GET http://localhost:5000/api/materials/<string:id>
##  NB: This returns an image object on success or a generic error on failure;


##  Required Flask Packages;;
from flask import Flask, send_file
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

##  Required Database
import rethinkdb as r
##  Required Python Packages;
import json, uuid, sys, werkzeug, os

## Custom Helper Functions
from functions import *


class getmaterials(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(getmaterials, self).__init__()

    ## HTTP GET METHOD
    def get(self, id):
        ## build local path to image;
        pathTo = os.path.join("uploaded/", id)
        ## return the raw file using Flask;
        return send_file(pathTo)
        

    ## HTTP DELETE METHOD
    def delete(self):
        pass

    ## HTTP PUT METHOD
    def put(self):
        pass

    ## HTTP POST METHOD
    def post(self):
        pass
