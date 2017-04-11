
##  userfavourite.py
##
##  provides the user's beacons endpoint;
##
##  ENDPOINT: /api/user/favourite
##  REST STATES: GET, POST
##
##  Input:
##  user_id - found in the JSON component of the request.
##  store_id - found in the JSON component of the request.
##
##  Example: GET
##  curl -H "Content-Type: application/json" -X GET -d '{"user_id": <string:user_id>}' http://localhost:5000/api/user/favourite
##
##  Example: POST
##  curl -H "Content-Type: application/json" -X POST -d '{"user_id": <string:user_id>, "store_id": <string:store_id>}' http://localhost:5000/api/user/favourite


##  Required Flask Packages;;
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Customer Helper Functions
from functions import *

class userfavourite(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(userfavourite, self).__init__()

    ##  HTTP GET METHOD
    ##  onFailure => []
    ##  onSuccess => Document
    ##  Document:
    ##  {
    ##    "favouritestores": ArrayOf<StoreDocument> ,
    ##    "id":  <string>,
    ##    "user_id":  <string>
    ##  }
    ##  Store Document:
    ## {
    ##     "beacons": ArrayOf<String>,
    ##     "id": <String>,
    ##     "lat": <String>,
    ##     "long": <String>,
    ##     "name": <String>,
    ##     "promotion": {
    ##         "active": <String>,
    ##         "coupon": <String>,
    ##         "expires":<String>,
    ##         "id": <String>,
    ##         "message": <String>,
    ##         "present": <String>,
    ##         "promotionImage":<String>,
    ##         "promotion_id":<String>,
    ##         "store_id":<String>,
    ##         "title":<String>,
    ##     },
    ##     "store_id":<String>,
    ##     "store_manager_id":<String>,
    ## }
    def get(self):
        self.reqparse.add_argument("user_id", type=str, required=True, help="User ID Not Defined.", location="json")
        args = self.reqparse.parse_args()
        initConnection()

        response = r.db("beaconrebuild").table("user_favouritestore").get_all(args["user_id"], index="user_id").run()

        ## okay for each user;
        document = []
        fs = []
        for user in response:
            ## use the single user to create
            for store in user["favouritestores"]:
                x = r.db("beaconrebuild").table("store").filter({"store_id": store}).run()
                # for each;
                for store in x:
                    z = r.db("beaconrebuild").table("store_promotion").filter({"store_id": store["store_id"], "active": "yes"}).run()
                    ## get the promotion object and bind it.;
                    for promo in z:
                        store["promotion"] = promo
                    fs.append(store)
            ## replace array of strings with objects
            user["favouritestores"] = fs
            return user

    ## HTTP DELETE METHOD
    def delete(self):
        pass

    ## HTTP PUT METHOD
    def put(self):
        pass

    ##  HTTP POST METHOD
    ##  onFailure => []
    ##      It will either throw an error or the ReqParser will catch any bad inputs;
    ##  onSuccess => []
    ##      the post is merely an update to add to data.
    def post(self):
        self.reqparse.add_argument("user_id", type=str, required=True, help="User ID Not Defined.", location="json")
        self.reqparse.add_argument("store_id", type=str, required=True, help="Store Id", location="json")
        args = self.reqparse.parse_args()
        initConnection()

        count = r.db("beaconrebuild").table("user_favouritestore").get_all(args["user_id"], index="user_id").count().run()
        ## insert a new row if this is te first time its being favourited.
        if (count <= 0):
            r.db("beaconrebuild").table("user_favouritestore").insert({"user_id": args["user_id"], "favouritestores": []}).run()

        # toJSON = json.loads(args["update"])

        ## append.
        r.db("beaconrebuild").table("user_favouritestore").get_all(args["user_id"],index="user_id").update({
            "favouritestores": r.row["favouritestores"].default([]).append(args["store_id"])
        }).run()

        return []
