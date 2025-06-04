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
        conn = sqlite3.connect(':memory:')
        for filename in os.listdir(DATA_FOLDER):
            if filename.endswith('.csv'):
                file_path = os.path.join(DATA_FOLDER, filename)
                if os.path.getsize(file_path) == 0:
                    continue
                try:
                    df = pd.read_csv(file_path)
                    if df.empty or df.columns.size == 0:
                        continue
                    table_name = os.path.splitext(filename)[0]
                    df.to_sql(table_name, conn, index=False, if_exists='replace')
                except Exception as e:
                    print(f"⚠️ Skipping {filename}: {e}")

        cursor = conn.cursor()
        cursor.execute(query)

        # Check if the query returns rows (i.e. SELECT query)
        if cursor.description is not None:
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return jsonify({'columns': columns, 'rows': rows})
        else:
            conn.commit()
            return jsonify({'message': '✅ Query executed successfully.'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
