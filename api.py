#
#   api.py
#   Command: sudo python api.py
#
#   Description:
#   api.py is our entry point for all of our connections. It is a RESTful server.



#  Server-Specific Packages;
from flask import Flask, send_file
from flask_restful import Api
from flask_cors import CORS, cross_origin
from flask.views import MethodView

# Python Specific Packages;
import json, uuid, sys, os

# Custom Packages
# for custom routes use the format
# from routes.<file_name> import <class_name>
from routes.skeleton import skeleton
from routes.serverinfo import ServerInformation
from routes.store import store
from routes.promotion import promotion
from routes.beacon import beacon
from routes.beaconstore import beaconstore
from routes.user import user
from routes.userstores import userstores
from routes.userstorepromotions import userstorepromotions
from routes.oauth import oauth
from routes.userbeaconinteraction import userbeaconinteraction
from routes.userbeacons import userbeacons
from routes.interactstat_store import interactstat_store
from routes.interactstat_userstore import interactstat_userstore
from routes.promotionalmaterials import promotionalmaterials
from routes.getmaterials import getmaterials
from routes.placeorder import placeorder
from routes.userfavourite import userfavourite

# Create Application
app = Flask(__name__, static_folder = "uploaded")

# set a static upload;
app.config["UPLOAD_FOLDER"] = "uploaded"

# send the cross_origin activity;
cors = CORS(app, resources={"*": {"origins": "*"}})
## For Debuging Purposes ONLY.
## We Need to Define A Class Specific catch 404 erros.
api = Api(app, catch_all_404s=True)

## These are all of our endpoints;

## To Add Custom Resources;
## api.add_resource(<class_name>, "<route_pattern>")
api.add_resource(skeleton, "/skeleton", "/skeleton/<int:id>")
api.add_resource(ServerInformation, "/api", "/api")
## User Endpoints;
api.add_resource(user, "/api/user", "/api/user/")
api.add_resource(oauth, "/api/user/oauth", "/api/user/oauth/")
api.add_resource(userstores, "/api/user/store", "/api/user/store/")
api.add_resource(userbeacons, "/api/user/beacons", "/api/user/beacons/")
api.add_resource(userfavourite, "/api/user/favourite", "/api/user/favourite/")
api.add_resource(userbeaconinteraction, "/api/user/interact/beacons", "/api/user/interact/beacons/")
api.add_resource(userstorepromotions, "/api/user/store/promotion", "/api/user/store/promotion/")
## Store Endpoints
api.add_resource(store, "/api/store", "/api/store/")
## Promotion Endpoints
api.add_resource(promotion, "/api/promotion", "/api/promotion/")
api.add_resource(promotionalmaterials, "/api/promotion/materials", "/api/promotion/materials/")
## Beacon Endpoints
api.add_resource(beacon, "/api/beacon", "/api/beacon/")
api.add_resource(beaconstore, "/api/beacon/store", "/api/beacon/store/")
## Stats Endpoints
api.add_resource(interactstat_store, "/api/stats/interact/store", "/api/stats/interact/store/")
api.add_resource(interactstat_userstore, "/api/stats/interact/user/store", "/api/stats/interact/user/store/")
## Misc. Endpoints
api.add_resource(placeorder, "/api/order", "/api/order/")
api.add_resource(getmaterials, "/api/materials/<string:id>")




## cURL example - just a reminder for testing purposes;
## Api Documentation more details.
## CURL example ;; BEACUSE I NEED IT
## curl -H "Content-Type: application/json" -X POST -d '{"store_manager_id": "4fdfec63-1629-4c7d-96d5-16b41490fb9e"}' http://localhost:5000/api/store


if __name__ == '__main__':
    ## Run it as a Live Server
    app.run(host='0.0.0.0', debug=True)
    ## Run it as a Local Server;
    #app.run(debug=True)
