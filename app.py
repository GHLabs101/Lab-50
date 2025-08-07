# app.py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

DATABASE = "demo.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT)")
    # Add a couple of demo rows
    cur.executemany("INSERT OR IGNORE INTO users(id, name) VALUES(?, ?)", [(1, "Alice"), (2, "Bob")])
    conn.commit()
    conn.close()

@app.route("/user")
def get_user():
    """
    ⚠️  Deliberately unsafe query so CodeQL will flag it.
    Visit /user?id=1   → returns {"id":1,"name":"Alice"}
    """
    user_id = request.args.get("id", "")
    # UNSAFE: string concatenation exposes risk of SQL injection
    query = f"SELECT id, name FROM users WHERE id = {user_id};"
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(query)
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify({"id": row[0], "name": row[1]})
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
