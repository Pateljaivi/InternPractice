from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

items = [
    {"id":1,"name":"laptop","price":1200},
    {"id":2,"name":"mouse","price":200}
]

@app.route("/items",methods=["GET"])
def get_items():
    return jsonify({"data":items}),200


if __name__ == "__main__":
    app.run(debug=True)