import os, sqlite3, time
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="web")
DB = "game.db"
MAX_ENERGY = 100
ENERGY_REGEN_SECONDS = 3

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = db()
    con.execute("""CREATE TABLE IF NOT EXISTS users(
        telegram_id INTEGER PRIMARY KEY,
        username TEXT,
        coins INTEGER NOT NULL DEFAULT 0,
        energy INTEGER NOT NULL DEFAULT 100,
        tap_power INTEGER NOT NULL DEFAULT 1,
        last_energy INTEGER NOT NULL,
        last_daily INTEGER NOT NULL DEFAULT 0
    )""")
    con.commit()
    con.close()

def regen(row):
    now = int(time.time())
    elapsed = max(0, now - row["last_energy"])
    energy = min(MAX_ENERGY, row["energy"] + elapsed // ENERGY_REGEN_SECONDS)
    return energy, now

def get_user(tg_id, username="Player"):
    con = db()
    row = con.execute("SELECT * FROM users WHERE telegram_id=?", (tg_id,)).fetchone()
    if row is None:
        now=int(time.time())
        con.execute("INSERT INTO users(telegram_id,username,last_energy) VALUES(?,?,?)",
                    (tg_id, username or "Player", now))
        con.commit()
        row = con.execute("SELECT * FROM users WHERE telegram_id=?", (tg_id,)).fetchone()
    energy, now = regen(row)
    if energy != row["energy"]:
        con.execute("UPDATE users SET energy=?,last_energy=? WHERE telegram_id=?",
                    (energy, now, tg_id))
        con.commit()
        row = con.execute("SELECT * FROM users WHERE telegram_id=?", (tg_id,)).fetchone()
    con.close()
    return row

@app.get("/")
def index():
    return send_from_directory("web", "index.html")

@app.get("/api/state")
def state():
    tg_id = request.args.get("telegram_id", type=int)
    username = request.args.get("username", "Player")
    if not tg_id:
        return jsonify({"error":"telegram_id required"}),400
    row=get_user(tg_id, username)
    return jsonify(dict(row))

@app.post("/api/tap")
def tap():
    data=request.get_json(force=True)
    tg_id=int(data["telegram_id"])
    row=get_user(tg_id, data.get("username","Player"))
    if row["energy"] <= 0:
        return jsonify({"ok":False,"error":"No energy"}),400
    new_energy=row["energy"]-1
    new_coins=row["coins"]+row["tap_power"]
    con=db()
    con.execute("UPDATE users SET coins=?,energy=?,last_energy=? WHERE telegram_id=?",
                (new_coins,new_energy,int(time.time()),tg_id))
    con.commit()
    con.close()
    return jsonify({"ok":True,"coins":new_coins,"energy":new_energy})

@app.post("/api/upgrade")
def upgrade():
    data=request.get_json(force=True)
    tg_id=int(data["telegram_id"])
    row=get_user(tg_id, data.get("username","Player"))
    cost=50*row["tap_power"]
    if row["coins"] < cost:
        return jsonify({"ok":False,"error":"Not enough coins","cost":cost}),400
    con=db()
    con.execute("UPDATE users SET coins=coins-?,tap_power=tap_power+1 WHERE telegram_id=?",
                (cost,tg_id))
    con.commit()
    con.close()
    return jsonify({"ok":True})

@app.post("/api/daily")
def daily():
    data=request.get_json(force=True)
    tg_id=int(data["telegram_id"])
    row=get_user(tg_id, data.get("username","Player"))
    now=int(time.time())
    if now-row["last_daily"] < 86400:
        return jsonify({"ok":False,"error":"Daily reward already claimed"}),400
    reward=500
    con=db()
    con.execute("UPDATE users SET coins=coins+?,last_daily=? WHERE telegram_id=?",
                (reward,now,tg_id))
    con.commit()
    con.close()
    return jsonify({"ok":True,"reward":reward})

@app.get("/api/leaderboard")
def leaderboard():
    con=db()
    rows=con.execute("SELECT username,coins FROM users ORDER BY coins DESC LIMIT 20").fetchall()
    con.close()
    return jsonify([dict(r) for r in rows])

if __name__=="__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT","5000")), debug=False)
