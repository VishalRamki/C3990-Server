
##  oauth.py
##
##  provides the oauth endpoint;
##
##  ENDPOINT: /api/user/oauth
##  REST STATES: GET
##
##  Input:
##  google_oauth_token - found in the locations
##
##
##
##  Example: GET
##  curl -H "Content-Type: application/json" -X <GET/DELETE> -d '{"google_oauth_token": <string:google_oauth_token>}' http://localhost:5000/api/user/oauth
##  NB This only confirms or disconfirms whether or not the system has the Merchant Registered. It doesn't not do the registration;


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

class oauth(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(oauth, self).__init__()

    ##  HTTP GET METHOD
    ##  onFailure => {"error": "1"}
    ##      this error response is Specific for the Merchant interface.
    ##      it allows the Merchant interface to perform the actions required to
    ##      enter the user.
    ##  onSuccess => [ArrayOf<Document>]
    ##      Document Example:
    ##      {
    ##          "user_id": <string>,
    ##          "id": <string>
    ##      }
    ##
    def get(self):
        self.reqparse.add_argument("google_oauth_token", type=str, required=False, help="No google_oauth_token Provided")
        args = self.reqparse.parse_args()
        initConnection()

        ## TODO Actually write the Google oAuth Token Validation here.
        bid = args["google_oauth_token"]
        print(bid)
        # get from rethink;
        isitthere = r.db("beaconrebuild").table("user").filter({"google_oauth_token": bid}).count().run()
        print(isitthere)
        ## determines if the user is not registered.
        if (isitthere <= 0):
            return {"error": "1"}

        ## user is registered.
        ntbl = r.db("beaconrebuild").table("user").get_all(bid, index="google_oauth_token").run()
        # print(ntbl)
        toJSON = []
        for doc in ntbl:
            ## remove the auth key for secruity reeasons;
            toJSON = removekey(doc, "google_oauth_token")
        # print(toJSON)
        return toJSON
        # return {"g":"g"}

    ## HTTP DELETE METHOD
    def delete(self):
        pass

    ## HTTP PUT METHOD
    def put(self):
        pass

    ## HTTP POST METHOD
    def post(self):
        pass
