import os
import re
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

def connect():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

conn = connect()
with conn.cursor() as cur:
    cur.execute("SELECT count(*) FROM leaked_hashes")
    print(f"W bazie jest {cur.fetchone()[0]} hashy", flush=True)
conn.close()

@app.post("/check")
def check():
    data = request.get_json(silent=True) or {}
    if "hash" not in data:
        return jsonify({"error": "brak pola 'hash'"}), 400
    h = str(data["hash"]).lower()
    if not re.fullmatch(r"[0-9a-f]{40}", h):
        return jsonify({"error": "pole 'hash' musi być skrótem SHA-1"}), 400
    print(f"check: hash={h[:5]}...", flush=True)

    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT EXISTS (SELECT 1 FROM leaked_hashes WHERE hash = %s)", (h,))
            found = cur.fetchone()[0]
    finally:
        conn.close()
    return jsonify({"found": found})

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)