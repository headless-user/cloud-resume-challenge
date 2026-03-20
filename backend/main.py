from fastapi import FastAPI
import sqlite3
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
)

def create_con():
    con = sqlite3.connect("visitors.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS v_count (
                id INTEGER PRIMARY KEY,
                act_count INTEGER
                )""")
    return con, cur



@app.get("/count")
def visitor_count():
    con, cur = create_con()
    count = cur.execute("SELECT act_count FROM v_count")
    count = cur.fetchone()
    if count is None:
        cur.execute("INSERT INTO v_count (act_count) VALUES (1)")
        count = 1 
    else:
        count = count[0] + 1
        cur.execute(f"UPDATE v_count SET act_count = {count}")
    con.commit()
    return count

