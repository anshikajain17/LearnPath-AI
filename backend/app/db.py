import json, os, sqlite3
from pathlib import Path

DB = Path(os.getenv("DATABASE_PATH","learnpath.db"))

def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    c = conn()
    c.execute("CREATE TABLE IF NOT EXISTS profiles (id INTEGER PRIMARY KEY, data TEXT NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS assessments (id INTEGER PRIMARY KEY AUTOINCREMENT, skill TEXT, score REAL)")
    c.commit(); c.close()

def save_profile(data):
    c=conn()
    c.execute("INSERT OR REPLACE INTO profiles(id,data) VALUES(1,?)",(json.dumps(data),))
    c.commit(); c.close()

def load_profile():
    c=conn(); row=c.execute("SELECT data FROM profiles WHERE id=1").fetchone(); c.close()
    return json.loads(row["data"]) if row else None

def save_assessment(skill, score):
    c=conn(); c.execute("INSERT INTO assessments(skill,score) VALUES(?,?)",(skill,score)); c.commit(); c.close()
