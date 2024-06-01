from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL configurations
def get_db_connection():
    return mysql.connector.connect(
        host="db",  # service name defined in docker-compose.yml
        port=3306,  # MySQL service port
        user="root",
        password="root",
        database="test_db"
    )

# Create a new user
@app.route('/users', methods=['POST'])
def add_user():
    new_user = request.json
    if not new_user or 'name' not in new_user or 'email' not in new_user:
        return jsonify({'error': 'Please provide name and email'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users(name, email) VALUES (%s, %s)", (new_user['name'], new_user['email']))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'User added!'}), 201

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(users)

# Get a specific user
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

# Update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    update_data = request.json
    if not update_data or ('name' not in update_data and 'email' not in update_data):
        return jsonify({'error': 'Please provide name or email to update'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    query = "UPDATE users SET "
    if 'name' in update_data:
        query += "name = %s "
    if 'email' in update_data:
        query += "email = %s "
    query += "WHERE id = %s"
    
    cursor.execute(query, (update_data.get('name'), update_data.get('email'), user_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'User updated!'})

# Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'User deleted!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

