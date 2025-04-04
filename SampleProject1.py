from flask import Flask, request, jsonify  # type: ignore
from flask_restful import Api, Resource  # type: ignore
from flask_cors import CORS  # type: ignore

app = Flask(__name__)
api = Api(app)
CORS(app)  # Enable Cross-Origin Resource Sharing

@app.route("/")
def home():
    return {"message": "Hello, World! This is a Flask API on Render."}

# Dummy database
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Doe", "email": "jane@example.com"}
]

class UserList(Resource):
    def get(self):
        """Get all users"""
        return users

    def post(self):
        """Create a new user"""
        data = request.get_json()
        new_user = {
            "id": len(users) + 1,
            "name": data["name"],
            "email": data["email"]
        }
        users.append(new_user)
        return {"message": "User added successfully", "user": new_user}, 201

class User(Resource):
    def get(self, user_id):
        """Get a user by ID"""
        user = next((user for user in users if user["id"] == user_id), None)
        if user:
            return user
        return {"message": "User not found"}, 404

    def put(self, user_id):
        """Update user details"""
        data = request.get_json()
        for user in users:
            if user["id"] == user_id:
                user["name"] = data.get("name", user["name"])
                user["email"] = data.get("email", user["email"])
                return {"message": "User updated", "user": user}
        return {"message": "User not found"}, 404

    def delete(self, user_id):
        """Delete a user"""
        global users
        users = [user for user in users if user["id"] != user_id]
        return {"message": "User deleted"}

# Define API routes
api.add_resource(UserList, "/users")
api.add_resource(User, "/users/<int:user_id>")

if __name__ == "__main__":
    app.run(debug=True)
