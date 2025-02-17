from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="db",  # Service name from docker-compose
        port="5432"
    )
    return conn

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 'Hello, World from PostgreSQL!'")
        message = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({"message": message})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
