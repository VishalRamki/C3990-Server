#  Python Packages
from flask import Flask
from flask_restful import Api

# Custom Packages
# for custom routes use the format
# from routes.<file_name> import <class_name>
from routes.skeleton import skeleton
from routes.serverinfo import ServerInformation
from routes.store import store
from routes.promotion import promotion
from routes.beacon import beacon
from routes.user import user
from routes.userbeaconinteraction import userbeaconinteraction

app = Flask(__name__)

## For Debuging Purposes ONLY.
## We Need to Define A Class Specific catch 404 erros.
api = Api(app, catch_all_404s=True)

## To Add Custom Resources;
## api.add_resource(<class_name>, "<route_pattern>")
api.add_resource(skeleton, "/skeleton", "/skeleton/<int:id>")
api.add_resource(ServerInformation, "/api", "/api")
api.add_resource(store, "/api/store", "/api/store/")
api.add_resource(promotion, "/api/promotion", "/api/promotion/")
api.add_resource(beacon, "/api/beacon", "/api/beacon/")
api.add_resource(user, "/api/user", "/api/user/")
api.add_resource(userbeaconinteraction, "/api/user/beacons", "/api/user/beacons/")



## CURL example ;; BEACUSE I NEED IT
## curl -H "Content-Type: application/json" -X POST -d '{"store_manager_id": "4fdfec63-1629-4c7d-96d5-16b41490fb9e"}' http://localhost:5000/api/store


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
