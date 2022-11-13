import sys
from flask import Flask, request

app = Flask(__name__)

@app.route("/hello", methods=["GET"])
def hello_world():
    if request.method == "GET":
        return "<p>Hello, world!</p>", 201

if __name__ == "__main__":
    app.run(debug=True)