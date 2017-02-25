from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

##
##  This is a skeleton which you can refer to when writing the routes for the
##  functions of the API.
##  This skeleton is very basic, but has the Argument Parser, All Four Major
##  RESTful functions.
##

def debug(object):
    print("API Was Requested with Object: ",object)

class skeleton(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        self.reqparse.add_argument("id", type =  int, required=True, help="No ID Provided", location="json")
        super(skeleton, self).__init__()

    ## HTTP GET METHOD
    def get(self, id):
        ## print the information for debugging purposes;
        debug(id)
        return {"api_request": "get", "object_requested": id}

    ## HTTP DELETE METHOD
    def delete(self, id):
        ## print the information for debugging purposes;
        debug(id)
        return {"api_request": "delete", "object_requested": id}

    ## HTTP PUT METHOD
    def put(self, id):
        ## print the information for debugging purposes;
        debug(id)
        return {"api_request": "put", "object_requested": id}

    ## HTTP POST METHOD
    def post(self, id):
        ## print the information for debugging purposes;
        debug(id)
        return {"api_request": "post", "object_requested": id}
