from flask import Flask, request, jsonify
import psycopg2
import socket
from retry import retry

app = Flask(__name__)

@retry(psycopg2.OperationalError, tries=3, delay=2)
def get_db_connection():
    conn = psycopg2.connect(
        host="db",  # Use 'localhost' if you're not using Docker
        # host="localhost",
        database="self_healing",
        user="postgres",
        password="Prasanna@31"
    )
    return conn

@app.route('/')
def home():
    return f"Hello from {socket.gethostname()}!"

@app.route('/health')
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return "UP", 200
    except:
        return "DB DOWN", 500

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Handle form or JSON input
        name = request.form.get("name")
        if not name and request.is_json:
            data = request.get_json()
            name = data.get("name")

        if not name:
            return jsonify({"error": "Name is required"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name) VALUES (%s);", (name,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": f"User '{name}' added"}), 201

    # If GET method: return HTML form
    return '''
        <h2>Add User</h2>
        <form action="/add" method="post">
            Name: <input type="text" name="name" required>
            <input type="submit" value="Add User">
        </form>
    '''

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
