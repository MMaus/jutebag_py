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

@server.route("/bagpy/todo/<userEmail>")
def fetchTodo(userEmail: str) -> str:
    todo = backend.fetchTodo(userEmail)
    response = flask.jsonify(todo)
    print("TodoList for " + userEmail + ": " + str(response))
    return response

@server.route("/bagpy/todo/<userEmail>", methods=["POST"])
def putTodo(userEmail: str) -> str:
    json = request.json
    todoData = {
        'version' : json.get(u'version'), # iteration of the todo list
        'tasks' : json.get(u'tasks'), # a nested dict
    }
        # 'tasklist' : json.get(u'tasklist'), # array (list) of tasks, each is { label: string, status: int}
        # 'nextActionTime' : json.get(u'nextActionTime'), # string, representing a data
        # 'label' : json.get(u'label'), # label of the todo item
    result = backend.storeTodo(userEmail, todoData)
    response = flask.jsonify(result)
    return response

@server.route("/bagpy/joinRequests/<userEmail>")
def pendingRequests(userEmail: str) -> str:
    requests = backend.getJoinRequests(userEmail)
    response = flask.jsonify(requests)
    print("Pending requests for " + userEmail + ": " + str(response))
    return response


@server.route("/bagpy/v2/<userEmail>", methods=["GET"])
def storeBagv2(userEmail):
    bag = backend.fetchBag_v2(userEmail)
    print("fetched bag for user " + userEmail)
    return flask.jsonify(bag)

@server.route("/bagpy/v2/<userEmail>", methods=["POST"])
def fetchBagv2(userEmail):
    json = request.json
    storeData = {
        'categories' : json.get(u'categories'),
        'items' : json.get(u'items'),
        'revision' : json.get(u'revision')
    }
    return flask.jsonify(backend.storeBag_v2(userEmail, storeData))

@server.route("/bagpy/<userEmail>")
def fetchBag(userEmail: str) -> str:
    bag = backend.fetchBag_v1(userEmail)
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
    return flask.jsonify(backend.storeBag_v1(userEmail, storeData))

if __name__ == "__main__":
    print("trying to start stuff")
    server.run(host='0.0.0.0', port=8000)
    print("stuff started")
