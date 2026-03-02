from flask import Flask,request, jsonify,abort

app = Flask(__name__)

items = [
    {"id":1,"name":"laptop","price":1200},
    {"id":2,"name":"mouse","price":200}
]

#1.get items
@app.route("/items",methods=["GET"])
def get_items():
    return jsonify({"data":items}),200

#2.specific item
@app.route("/items/<int:item_id>",methods=["GET"])
def get_item(item_id):
    item = next((i for i in items if i["id"] == item_id),None)
    if item is None:
        abort(404,description="Item not found")
    return jsonify(item),200


#3.create
@app.route("/items",methods = ["POST"])
def create_item():
    if not request.json or "name" not in request.json:
        abort(400,description="Invalid data")

    new_item = {
        "id": items[-1]["id"] +1,
        "name": request.json["name"],
        "price": request.json.get("price",0)
    }

    items.append(new_item)
    return jsonify(new_item),201

#4.delete

@app.route("/items/<int:item_id>",methods = ["DELETE"])
def delete_item(item_id):
    global items
    items = [i for i in items if i["id"] != item_id]
    return jsonify({"result":True}),200



if __name__ == "__main__":
    app.run(debug=True)