from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r


##
##  This is a skeleton which you can refer to when writing the routes for the
##  functions of the API.
##  This skeleton is very basic, but has the Argument Parser, All Four Major
##  RESTful functions.
##
## example: UUID: 3295-23532-22156

# for debuging


class store(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(store, self).__init__()

    ## HTTP GET METHOD
    def get(self):
        self.reqparse.add_argument("uuid", type =  str, required=True, help="No UUID Provided", location="json")
        self.reqparse.add_argument("store_id", type =  str, required=True, help="No Store ID Provided", location="json")
        args = self.reqparse.parse_args();
        r.connect("localhost", 28015).repl()
        print("uuid: ",args["uuid"])
        print("store_id: ", args["store_id"])
        uuid = args["uuid"]
        store_id = args["store_id"]
        # get from rethink;
        nuuid = uuid.replace("-","_")
        store_tbl = "store_" + nuuid
        ntbl = r.db("stores").table(store_tbl).get_all(uuid, index="uuid").run()
        # print(ntbl)
        i = 0
        finalJSON = ""
        for item in ntbl:
            finalJSON = item
        print(finalJSON)
        return finalJSON

    ## HTTP DELETE METHOD
    def delete(self):
        pass

    ## HTTP PUT METHOD
    def put(self):
        pass

    ## HTTP POST METHOD
    def post(self):
        self.reqparse.add_argument("type", type=str, required=True, help="Function Not Defined", location="json")
        self.reqparse.add_argument("manager", type=str, required=True, help="Store Manager Not Defined", location="json")
        self.reqparse.add_argument("uuid", type=str, required=True, help="No UUID Provided", location="json")
        args = self.reqparse.parse_args()
        print("Type: ", args["type"])
        print("UUID: ", args["uuid"])
        print("Store_Manager: ", args["manager"])
        # get the data from the db;
        r.connect("localhost", 28015).repl()


        return {}
        pass
