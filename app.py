import json
from flask import Flask, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://chat.openai.com"}})

_TODOS = {}

@app.route("/todos/<string:username>", methods=['POST'])
def add_todo(username):
    request_data = request.get_json(force=True)
    if username not in _TODOS:
        _TODOS[username] = []
    _TODOS[username].append(request_data["todo"])
    return 'OK', 200

@app.route("/todos/<string:username>", methods=['GET'])
def get_todos(username):
    return json.dumps(_TODOS.get(username, [])), 200

@app.route("/todos/<string:username>", methods=['DELETE'])
def delete_todo(username):
    request_data = request.get_json(force=True)
    todo_idx = request_data["todo_idx"]
    if 0 <= todo_idx < len(_TODOS[username]):
        _TODOS[username].pop(todo_idx)
    return 'OK', 200

@app.route("/logo.png", methods=['GET'])
def plugin_logo():
    filename = 'logo.png'
    return send_file(filename, mimetype='image/png')

@app.route("/.well-known/ai-plugin.json", methods=['GET'])
def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return text, 200, {'Content-Type': 'text/json'}

@app.route("/openapi.yaml", methods=['GET'])
def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return text, 200, {'Content-Type': 'text/yaml'}

def main():
    app.run(debug=True, host="0.0.0.0", port=3333)

if __name__ == "__main__":
    main()
