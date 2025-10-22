import json
import os

from flask import Flask
from flask import jsonify
from flask import request

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load favorite foods from netids folder
def load_favorite_foods():
    """
    Reads all .txt files in the netids folder and extracts netid and favorite food.
    Returns a dictionary mapping netid to favorite food.
    """
    foods = {}
    netids_folder = "netids"
    
    if not os.path.exists(netids_folder):
        return foods
    
    for filename in os.listdir(netids_folder):
        if filename.endswith(".txt"):
            netid = filename[:-4]  # Remove .txt extension
            filepath = os.path.join(netids_folder, filename)
            
            try:
                with open(filepath, 'r') as f:
                    first_line = f.readline().strip()
                    if first_line:
                        foods[netid] = first_line
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    return foods

# Initialize favorite foods
favorite_foods = load_favorite_foods()


@app.route("/")
def hello_world():
    return "Hello world!"


@app.route("/foods/")
def get_foods():
    """
    Returns all netids and their favorite foods
    """
    foods_list = [{"netid": netid, "food": food} for netid, food in favorite_foods.items()]
    res = {"foods": foods_list}
    return json.dumps(res), 200


@app.route("/foods/<netid>/")
def get_food(netid):
    """
    Returns a favorite food by netid
    """
    food = favorite_foods.get(netid)
    if not food:
        return json.dumps({"error": "NetID not found"}), 404
    return json.dumps({"netid": netid, "food": food}), 200


@app.route("/foods/", methods=["POST"])
def create_food():
    """
    Adds a new netid and favorite food
    """
    body = json.loads(request.data)
    netid = body["netid"]
    food = body["food"]
    
    if netid in favorite_foods:
        return json.dumps({"error": "NetID already exists"}), 400
    
    favorite_foods[netid] = food
    return json.dumps({"netid": netid, "food": food}), 201


@app.route("/foods/<netid>/", methods=["POST"])
def update_food(netid):
    """
    Updates a favorite food by netid
    """
    if netid not in favorite_foods:
        return json.dumps({"error": "NetID not found"}), 404
    
    body = json.loads(request.data)
    food = body["food"]
    favorite_foods[netid] = food
    return json.dumps({"netid": netid, "food": food}), 200


@app.route("/foods/<netid>/", methods=["DELETE"])
def delete_food(netid):
    """
    Deletes a netid and favorite food
    """
    food = favorite_foods.get(netid, None)
    if not food:
        return json.dumps({"error": "NetID not found"}), 404
    
    del favorite_foods[netid]
    return json.dumps({"netid": netid, "food": food}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)