from flask import Flask, url_for, request, redirect, abort, jsonify, session
from StockDAO import stockDAO

app = Flask(__name__, 
static_url_path="", 
static_folder="staticpages")



@app.route("/")
def index():
  return ()


# get all 
# curl "http://127.0.0.1:5000/stocks"

@app.route("/stocks")
def getAll():
    results = stockDAO.getAll()
    return jsonify(results)

# find by id
#  curl "http://127.0.0.1:5000/stocks/2"
@app.route("/stocks/<int:id>")
def findById(id):
    foundStock = stockDAO.findByID(id)
    return jsonify(foundStock)


# create
# curl -X POST -H "content-type:application/json" -d "{\"item\":\"test\", \"category\":\"n/a\", \"price\":123}" http://127.0.0.1:5000/stocks

@app.route("/stocks", methods = ["POST"])
def create():

    #global nextId
    if not request.json:
        abort(400)

    stock = {
        # "id" : nextId, this is depricated

        "item" : request.json["item"],
        "category" : request.json["category"],
        "price" : request.json["price"]
    }
    # nextId += 1

    values = (stock["item"], stock["category"], stock["price"])
    newId = stockDAO.create(values)
    stock["id"] = newId
    return jsonify(stock)

# update
# curl -X PUT -d "{\"item\":\"category\", \"price\":999}" -H Content-Type:application/json http://127.0.0.1:5000/stocks/4

@app.route("/stocks/<int:id>", methods = ["PUT"])
def update(id):
    foundStock = stockDAO.findByID(id)
    if not foundStock:
        abort(404)

    reqJson = request.json

    if "item" in reqJson:
        foundStock["item"] = reqJson["item"]
    
    if "category" in reqJson:
        foundStock["category"] = reqJson["category"]

    if "price" in reqJson:
        foundStock["price"] = reqJson["price"]

    values = (foundStock["item"], foundStock["category"], foundStock["price"], foundStock["id"])
    stockDAO.update(values)
    return jsonify(foundStock)

# delete
# curl -X DELETE http://127.0.0.1:5000/stocks/5

@app.route("/stocks/<int:id>", methods = ["DELETE"])
def delete(id):
    stockDAO.delete(id)
    return jsonify({"done": True})

if __name__== "__main__":
  app.run(debug=True)