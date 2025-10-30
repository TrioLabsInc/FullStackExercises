from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)
DATABASE = "notes.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, text TEXT)")
    db.commit()


@app.route("/create_note", methods=["GET", "POST"])
def create_note():
    db = get_db()

    notes = db.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    return render_template("create_notes.html", notes=notes)

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)
