# C3990-Server

The Server code which is responsible for interfacing our [Android App]("https://www.github.com/VishalRamki/C3990") as well as our Web-based Client. It is built on Python, Flask and RethinkDB.

## Setting Up The Development Environment

1. Setup the git repo locally via the GitHub Desktop app.
2. Once that is done, make sure the dependances are installed via PIP: Flask, flask-restful.

```
pip install flask
pip install flask-restful
```

3. Run the python script via:

```
py api.py
```

The way Flask is setup, it allows you to make modifications to the code and reloads it.

# Changelog

### 08/04/17 - Massive Updated;

- The Entire System was redone.
- Added many new endpoints.
- Changed the way JSON is returned and accepted.
- Created a File Upload Endpoint.
- Refactored the code.

### 20/03/17 - Added New Routes [user, beacon, userbeaconinteraction]

This brings our server to BETA completion. There is all the basic functionalities which will allow the apps to begin working.

- Added new routes and endpoints, `/api/user`, `/api/beacon`, `/api/user/beacons`
- REST methods implemented, however not all the REST functions are implemented for all the endpoints. (This is by design)
- All the functions are raw input/ouput, no sorting or anything liek that.


### 15/03/17 - Addition Of New Routes [store, promotion]

- Added new routes and endpoints which correspond to the `/api/store` and `/api/promotion`
- All four REST methods implemented for both store and promotion.
- Store and Promotion deals with a single store or promotion. Additional classes will be written for sorting and the like.
- General Bugfixing

### 25/02/17 - Skeleton and Reorganization

- Reorganized the file structure.
- Included extra debug code.
- Provided an example of a route, with as much stuff as we may need. There is still other things that are needed.
