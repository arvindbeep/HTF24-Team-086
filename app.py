from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meal_planner.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    dietary_preferences = db.Column(db.String(255), nullable=True)

# Create the database
with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'], dietary_preferences=data.get('dietary_preferences'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User  registered successfully!"}), 201

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    # Here you can implement logic to send an email or store the message in the database
    print(f"Contact message from {data['name']} ({data['email']}): {data['message']}")
    return jsonify({"message": "Message sent successfully!"}), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{"id": user.id, "name": user.name, "email": user.email, "dietary_preferences": user.dietary_preferences} for user in users]
    return jsonify(user_list), 200

if __name__ == '__main__':
    app.run(debug=True)from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meal_planner.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    dietary_preferences = db.Column(db.String(255), nullable=True)

    def __init__(self, name, email, dietary_preferences=None):
        self.name = name
        self.email = email
        self.dietary_preferences = dietary_preferences

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "dietary_preferences": self.dietary_preferences
        }

# Create the database
with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if 'name' not in data or 'email' not in data:
        return jsonify({"message": "Name and email are required"}), 400
    new_user = User(name=data['name'], email=data['email'], dietary_preferences=data.get('dietary_preferences'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    if 'name' not in data or 'email' not in data or 'message' not in data:
        return jsonify({"message": "Name, email, and message are required"}), 400
    # Here you can implement logic to send an email or store the message in the database
    print(f"Contact message from {data['name']} ({data['email']}): {data['message']}")
    return jsonify({"message": "Message sent successfully!"}), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.to_dict()), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.dietary_preferences = data.get('dietary_preferences', user.dietary_preferences)
    db.session.commit()
    return jsonify(user.to_dict()), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)