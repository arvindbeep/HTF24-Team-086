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
    app.run(debug=True)