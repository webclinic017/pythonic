# ref: https://stackoverflow.com/questions/41831929/debug-flask-server-inside-jupyter-notebook

# README
# you can runs this inside a jupyter notebook for short demos. 
#    

from werkzeug.wrappers import Request, Response
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

names = []

@app.route("/test")
def testapp():
    return "I am working fine."

@app.route("/names")
def names():
    return names

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 9000, app)