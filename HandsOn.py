from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Create an in-memory SQLite database with some demo data
def init_db():
    conn = sqlite3.connect('sample.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        );
    ''')
    # Insert sample data
    cur.execute("INSERT INTO students (name, age) VALUES ('Alice', 22)")
    cur.execute("INSERT INTO students (name, age) VALUES ('Bob', 20)")
    cur.execute("INSERT INTO students (name, age) VALUES ('Charlie', 25)")
    conn.commit()
    conn.close()

# Route to serve the practice page
@app.route('/practice')
def practice():
    return render_template('practice.html')

# Endpoint to execute a SQL query sent from frontend
@app.route('/run_query', methods=['POST'])
def run_query():
    user_query = request.json.get('query')

    try:
        conn = sqlite3.connect('sample.db')
        cur = conn.cursor()
        cur.execute(user_query)

        # Fetch results if SELECT
        if user_query.strip().lower().startswith("select"):
            columns = [description[0] for description in cur.description]
            rows = cur.fetchall()
            result = {
                "columns": columns,
                "rows": rows
            }
        else:
            conn.commit()
            result = {"message": "Query executed successfully."}
        conn.close()
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
