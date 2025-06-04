from flask import Flask, request, jsonify
import pandas as pd
import sqlite3
import os

app = Flask(__name__)

DATA_FOLDER = os.path.join(os.getcwd(), 'data')

@app.route('/run_query', methods=['POST'])
def run_query():
    query = request.json.get('query', '')

    try:
        # Load all CSV files into SQLite in-memory DB
        conn = sqlite3.connect(':memory:')
        for filename in os.listdir(DATA_FOLDER):
            if filename.endswith('.csv'):
                table_name = os.path.splitext(filename)[0]
                df = pd.read_csv(os.path.join(DATA_FOLDER, filename))
                df.to_sql(table_name, conn, index=False, if_exists='replace')

        # Execute the query
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        return jsonify({'columns': columns, 'rows': rows})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
