from flask import Flask, render_template, request, jsonify
import pandas as pd
import sqlite3
import os

app = Flask(__name__)

DATA_FOLDER = os.path.join(os.getcwd(), 'dataset')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sqlquery')
def sqlquery():
    return render_template('SQLquery.html')

@app.route('/practice')
def practice():
    return render_template('practice.html')

@app.route('/run_query', methods=['POST'])
def run_query():
    query = request.json.get('query', '')
    try:
        # 🧠 Create in-memory SQLite DB
        conn = sqlite3.connect(':memory:')
        for filename in os.listdir(DATA_FOLDER):
            if filename.endswith('.csv'):
                file_path = os.path.join(DATA_FOLDER, filename)
                if os.path.getsize(file_path) == 0:
                    continue  # Skip empty files
                try:
                    df = pd.read_csv(file_path)
                    if df.empty or df.columns.size == 0:
                        continue  # Skip files with no columns
                    table_name = os.path.splitext(filename)[0]
                    df.to_sql(table_name, conn, index=False, if_exists='replace')
                except Exception as e:
                    print(f"⚠️ Skipping {filename}: {e}")


        # 🔍 Execute user query
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        return jsonify({'columns': columns, 'rows': rows})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
