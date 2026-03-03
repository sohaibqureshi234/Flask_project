from flask import Flask, jsonify, request
from db import tasks_collection, users_collection
from passlib.hash import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from passlib.hash import sha256_crypt  # <-- change here




app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # change this in production
jwt = JWTManager(app)



@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if users_collection.find_one({"username": username}):
        return {"error": "User already exists"}, 400

    # Hash password with sha256_crypt
    hashed_pw = sha256_crypt.hash(password)
    users_collection.insert_one({"username": username, "password": hashed_pw})
    return {"message": "User registered successfully"}, 201

# ------------------------
# LOGIN
# ------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = users_collection.find_one({"username": username})
    if not user:
        return {"error": "User not found"}, 404

    # Verify password
    if not sha256_crypt.verify(password, user["password"]):
        return {"error": "Invalid credentials"}, 401

    access_token = create_access_token(identity=username)
    return {"access_token": access_token}, 200
# ------------------------
# GET all tasks
# ------------------------
@app.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    tasks = list(tasks_collection.find({}, {"_id": 0}))
    return jsonify(tasks)

# ------------------------
# GET single task by name
# ------------------------
@app.route("/tasks/<task_name>", methods=["GET"])
def get_task(task_name):
    task = tasks_collection.find_one({"name": task_name}, {"_id": 0})
    if task:
        return jsonify(task)
    else:
        return jsonify({"error": "Task not found"}), 404

# ------------------------
# POST a new task
# ------------------------
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    task_name = data.get("name")
    if task_name:
        tasks_collection.insert_one({"name": task_name})
        return jsonify({"message": f"Task '{task_name}' added!"}), 201
    else:
        return jsonify({"error": "Task name is required"}), 400

# ------------------------
# PUT / update a task
# ------------------------
@app.route("/tasks/<task_name>", methods=["PUT"])
def update_task(task_name):
    data = request.get_json()
    new_name = data.get("name")
    if not new_name:
        return jsonify({"error": "New task name is required"}), 400

    result = tasks_collection.update_one(
        {"name": task_name},
        {"$set": {"name": new_name}}
    )

    if result.matched_count:
        return jsonify({"message": f"Task '{task_name}' updated to '{new_name}'"})
    else:
        return jsonify({"error": "Task not found"}), 404

# ------------------------
# DELETE a task
# ------------------------
@app.route("/tasks/<task_name>", methods=["DELETE"])
def delete_task(task_name):
    result = tasks_collection.delete_one({"name": task_name})
    if result.deleted_count:
        return jsonify({"message": f"Task '{task_name}' deleted"})
    else:
        return jsonify({"error": "Task not found"}), 404

# ------------------------
# Run server
# ------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5001)
