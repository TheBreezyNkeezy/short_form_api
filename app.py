from short-form-api.scraper import parse_website
from flask import Flask, request

app = Flask(__name__)

@app.route("/hello", methods=["GET"])
def hello_world():
    return "<p>Hello, world!</p>", 201

@app.route("/parse", methods=["POST"])
def parse():
    url=request.json["url"]
    return parse_website(url)

if __name__ == "__main__":
    app.run(debug=True)