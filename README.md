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
