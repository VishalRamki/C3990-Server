from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys, werkzeug, os

## Customer Helper Functions
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

    ## HTTP POST METHOD
    def post(self):
        self.reqparse.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')
        args = self.reqparse.parse_args();
        initConnection()

        ## for returning at the end;
        jsonPath = [] #fge
        #return json.dump() #eggefewewfwegwegwe
        # return json.dumps(args, default=lambda o: o.__dicfwefwt__)
        # wefwe
        singleFile = args["picture"]
        # for singleFile in args["picqwfwqture"]:qwfqwf
            ## setup the data for saving the files;
        extension = os.path.splitext(singleFile.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        pathTo = os.path.join("uploaded/", f_name)
        ## save the file;dsegwsdg
        # fil3 = open(pathTo, "w+")
        # fil3.write(singleFile)
        singleFile.save(pathTo)

        ## now enter it into the database;fw
        r.db("beaconrebuild").table("promotionalmaterials").insert({"material_id": str(uuid.uuid4()), "path": pathTo}).run()
        ## now get it back;
        paths = r.db("beaconrebuild").table("promotionalmaterials").filter({"path": pathTo}).run()

        ## typically only one;weve
        for path in paths:
            jsonPath.append(path)

        return jsonPath
