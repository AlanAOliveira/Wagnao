
from flask import Flask, request, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)


@app.route('/api/part', methods=['POST'])
def process_post_parts():
    data = request.get_json()
    if data:
        save_part_to_db(data)

        response = {
            'status': 'success',
            'message': 'Data received',
            'data': data
        }
            
        return jsonify(response), 200
  
    print(f"Received data: {data}")
    # Process the incoming data

@app.route('/api/parts', methods=['GET'])
def get_parts():
    db_file = 'app.db'
    with sqlite3.connect(db_file) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM parts')
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        parts = [dict(zip(columns, row)) for row in rows]
    return jsonify(parts), 200

def save_part_to_db(part):
    db_file = 'app.db'
    with sqlite3.connect(db_file) as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS parts (
                CodBarras TEXT PRIMARY KEY,
                Nome TEXT,
                Descricao TEXT,
                Imagem TEXT,
                Fornecedor TEXT,
                PrecoVenda REAL,
                PrecoCompra REAL,
                UnidadeMetro TEXT,
                EstoqueMinimo INTEGER,
                DataValidade TEXT,
                Categoria TEXT
            )
        ''')
        cur.execute('''
            INSERT OR REPLACE INTO parts (
                CodBarras, Nome, Descricao, Imagem, Fornecedor,
                PrecoVenda, PrecoCompra, UnidadeMetro, EstoqueMinimo, DataValidade, Categoria
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            part.get('CodBarras'),
            part.get('Nome'),
            part.get('Descricao'),
            part.get('Imagem'),
            part.get('Fornecedor'),
            float(part.get('PrecoVenda', 0)) if part.get('PrecoVenda') is not None else None,
            float(part.get('PrecoCompra', 0)) if part.get('PrecoCompra') is not None else None,
            part.get('UnidadeMetro'),
            int(part.get('EstoqueMinimo', 0)) if part.get('EstoqueMinimo') is not None else None,
            part.get('DataValidade'),
            part.get('Categoria'),
        ))
        conn.commit()


@app.route('/api/part/download', methods=['GET'])
def download_parts():
    db_file = 'app.db'
    with sqlite3.connect(db_file) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM parts')
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        parts = [dict(zip(columns, row)) for row in rows]

    pd.DataFrame(parts).to_csv('parts.csv', index=False)
    return open('parts.csv', encoding='utf-8').read(), 200, {'Content-Type': 'text/csv'}


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200



@app.route('/', methods=['GET'])
def index():
    return open('index.html', encoding='utf-8').read(), 200, {'Content-Type': 'text/html'}

@app.route('/front/dashboard', methods=['GET'])
def dashboard():
    return open('front/dashboard.html', encoding='utf-8').read(), 200, {'Content-Type': 'text/html'}

@app.route('/management/stock', methods=['GET'])
def stock_management():
    return open('management/stock.html', encoding='utf-8').read(), 200, {'Content-Type': 'text/html'}

@app.route('/management/parts', methods=['GET'])
def parts_management():
    return open(file='management/parts.html', encoding='utf-8').read(), 200, {'Content-Type': 'text/html'}


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, host='localhost', port=5000)

    