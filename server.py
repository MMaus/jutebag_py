from flask import Flask
import flask
from flask import request
import firebase_admin 
import firebase_admin.firestore as firestore

from app.jutebag.backend import JutebagBackend

backend = JutebagBackend("cred/jutebag-py-firebase-cred.json")

server = Flask(__name__, 
    static_url_path='/',
    static_folder="web/static",
    template_folder="web/templates")

@server.route("/")
def hello():
    return "Hello, Python"

@server.route("/bagpy/joinRequests/<userEmail>")
def pendingRequests(userEmail: str) -> str:
    requests = backend.getJoinRequests(userEmail)
    response = flask.jsonify(requests)
    print("Pending requests for " + userEmail + ": " + str(response))
    return response

@server.route("/bagpy/todo/<userEmail>")
def fetchTodo(userEmail: str) -> str:
    requests = backend.getJoinRequests(userEmail)
    response = flask.jsonify(requests)
    print("TodoList for " + userEmail + ": " + str(response))
    return response

@server.route("/bagpy/<userEmail>")
def fetchBag(userEmail: str) -> str:
    bag = backend.fetchBag(userEmail)
    print("bag for user " + userEmail + " = " + str(bag))
    return flask.jsonify(bag)

@server.route("/bagpy/<userEmail>", methods=["POST"])
def storeBag(userEmail):
    json = request.json
    storeData = {
        'categories' : json.get(u'categories'),
        'items' : json.get(u'items'),
        'revision' : json.get(u'revision')
    }
    return flask.jsonify(backend.storeBag(userEmail, storeData))

if __name__ == "__main__":
    print("trying to start stuff")
    server.run(host='0.0.0.0')
    print("stuff started")
