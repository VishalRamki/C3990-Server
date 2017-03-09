#  Python Packages
from flask import Flask
from flask_restful import Api

# Custom Packages
# for custom routes use the format
# from routes.<file_name> import <class_name>
from routes.skeleton import skeleton
from routes.serverinfo import ServerInformation
from routes.store import store

app = Flask(__name__)

## For Debuging Purposes ONLY.
## We Need to Define A Class Specific catch 404 erros.
api = Api(app, catch_all_404s=True)

## To Add Custom Resources;
## api.add_resource(<class_name>, "<route_pattern>")
api.add_resource(skeleton, "/skeleton", "/skeleton/<int:id>")
api.add_resource(ServerInformation, "/api", "/api")
api.add_resource(store, "/api/store", "/api/store/")

if __name__ == '__main__':
    app.run(debug=True)
