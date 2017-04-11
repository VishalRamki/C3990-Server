
##  beacon.py
##
##  provides the beacon endpoint;
##
##  ENDPOINT: /api/beacon
##  REST STATES: GET, DELETE, PUT, POST
##
##  Input:
##  beacon_id - found in the JSON component of the request.
##  beacon_uuid - found in the JSON component of the request.
##  beacon_major - found in the JSON component of the request.
##  beacon_minor - found in the JSON component of the request.
##  update - found in the JSON component of the request.
##
##  Example: GET, DELETE
##  curl -H "Content-Type: application/json" -X <GET/DELETE> -d '{"beacon_id": <string:beacon_id>}' http://localhost:5000/api/beacon
##
##  Example: PUT
##  curl -H "Content-Type: application/json" -X PUT -d '{"beacon_id": "<string:beacon_id>", "update": <string:json_object_that_stringified>}' http://localhost:5000/api/beacon
##  NB: "UPDATE" requires a stringified JSON Object which contains the key-value pairs for the fields which you want to update. See the GET Response to see what you can modifiy
##
##  Example: POST
##  curl -H "Content-Type: application/json" -X POST -d '{"beacon_uuid": <string:beacon_uuid>, "beacon_major": <string:beacon_major>, "beacon_minor": <string:beacon_minor>}' http://localhost:5000/api/beacon

##  Required Flask Packages;;
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

##  Required Database
import rethinkdb as r
##  Required Python Packages;
import json, uuid, sys

## Custom Helper Functions
from functions import *

## beacon class;
class beacon(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(beacon, self).__init__()

    ##  HTTP GET METHOD
    ##  onFailure => []
    ##  onSuccess => [
    ##      {
    ##      "beacon_id": <string>,
    ##      "claimed": <string>,
    ##      "id": <string>,
    ##      "major": <string>,
    ##      "minor": <string>,
    ##      "owner": <string>,
    ##      "uuid": <string>
    ##      }
    ##  ]
    def get(self):
        self.reqparse.add_argument("beacon_id", type =  str, required=True, help="No Beacon ID Provided", location="json")
        args = self.reqparse.parse_args();
        initConnection()
        print("beacon_id: ", args["beacon_id"])
        bid = args["beacon_id"]
        # get from rethink;
        ntbl = r.db("beaconrebuild").table("beacon").get_all(bid, index="beacon_id").run()
        print(ntbl)
        return returnJSON(ntbl)

    ##  HTTP DELETE METHOD
    ##  onFailure => []
    ##      Will not happen.
    ##  onSuccess => {
    ##      "deleted": <string:beacon_id>
    ##  }
    def delete(self):
        self.reqparse.add_argument("beacon_id", type=str, required=True, help="Beacon ID Not Defined.", location="json")
        args = self.reqparse.parse_args()
        initConnection()
        r.db("beaconrebuild").table("beacon").get_all(args["beacon_id"], index="beacon_id").delete().run()
        return {"deleted": args["beacon_id"]}

    ##  HTTP PUT METHOD
    ##  onFailure => {
    ##      "message": {
    ##          "content": "There is no Beacon with that ID"
    ##       }
    ##  }
    ##  onSuccess => Returns the updated Document, enclosed in an array;
    def put(self):
        self.reqparse.add_argument("beacon_id", type=str, required=True, help="Beacon ID Not Defined.", location="json")
        self.reqparse.add_argument("update", type=str, required=True, help="JSON Update not Defined.", location="json")
        args = self.reqparse.parse_args()
        initConnection()
        # check if store_id exists in database;
        count = r.db("beaconrebuild").table("beacon").get_all(args["beacon_id"], index="beacon_id").count().run()
        if (count <= 0):
            return {"message": {
                "content": "There is No Beacon with that ID"
            }}
        else:
            toJSON = json.loads(args["update"].replace("'", '"'))
            print(args["update"])

            r.db("beaconrebuild").table("beacon").get_all(args["beacon_id"], index="beacon_id").update(toJSON).run()
            nv = r.db("beaconrebuild").table("beacon").get_all(args["beacon_id"], index="beacon_id").limit(1).run()
            # print(json.dumps(nv))
            return returnJSON(nv)

    ##  HTTP POST METHOD
    ##  onFailure => []
    ##      It will either throw an error or the ReqParser will catch any bad inputs;
    ##  onSuccess => [{}]
    ##      will return the newly created document encased in an array,
    ##      similar to how HTTP GET request was carried out
    def post(self):
        self.reqparse.add_argument("beacon_uuid", type=str, required=True, help="Beacon ID Not Defined.", location="json")
        self.reqparse.add_argument("beacon_major", type=str, required=True, help="JSON Update not Defined.", location="json")
        self.reqparse.add_argument("beacon_minor", type=str, required=True, help="JSON Update not Defined.", location="json")
        args = self.reqparse.parse_args()
        initConnection()
        ## generate new UUID for the beacon;
        beacon_id = str(uuid.uuid4())
        ## Insert the document;
        r.db("beaconrebuild").table("beacon").insert({
          "beacon_id": args["beacon_uuid"], ## theres a bug in our implemetnation, the beacon has to use its own UUID as its id.
          "uuid": args["beacon_uuid"],
          "major": args["beacon_major"],
          "minor": args["beacon_minor"],
          "claimed": "false",
          "owner": "null"
        }).run()
        ## gets the newly created beaocn document;
        isitthere = r.db("beaconrebuild").table("beacon").filter({"beacon_id": beacon_id}).limit(1).run()
        ## returns it in a JSON Friendly format;
        return returnJSON(isitthere)
