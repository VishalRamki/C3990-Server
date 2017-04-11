
##  promotionalmaterials.py
##
##  provides the promotion materials endpoint;
##
##  ENDPOINT: /api/promotion/materials
##  REST STATES: POST
##
##  Example: POST
##  N/A
##  NB This isn't like the other endpoints. This endpoint accepts raw data via FormData.

##  Required Flask Packages;;
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

##  Required Database
import rethinkdb as r
##  Required Python Packages;
import json, uuid, sys, werkzeug, os

## Custom Helper Functions
from functions import *


class promotionalmaterials(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(promotionalmaterials, self).__init__()

    ## HTTP GET METHOD
    def get(self):
        pass

    ## HTTP DELETE METHOD
    def delete(self):
        pass

    ## HTTP PUT METHOD
    def put(self):
        pass

    ##  HTTP POST METHOD
    ##  onFailure => []
    ##      It will throw an error. Returns 500 BAD REQUEST.
    ##  onSuccess => [{}]
    ##      {
    ##          "id": <string>,
    ##          "material_id": <string>,
    ##          "path": <string>
    ##      }
    def post(self):
        self.reqparse.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')
        args = self.reqparse.parse_args();
        initConnection()

        ## for returning at the end;
        jsonPath = []
        singleFile = args["picture"]
        ## setup the data for saving the files;
        extension = os.path.splitext(singleFile.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        pathTo = os.path.join("uploaded/", f_name)
        ## save the file;
        singleFile.save(pathTo)

        ## now enter it into the database;fw
        r.db("beaconrebuild").table("promotionalmaterials").insert({"material_id": str(uuid.uuid4()), "path": pathTo}).run()
        ## now get it back;
        paths = r.db("beaconrebuild").table("promotionalmaterials").filter({"path": pathTo}).run()

        ## typically only one
        for path in paths:
            jsonPath.append(path)

        return jsonPath
