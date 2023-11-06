from flask import Flask, render_template, jsonify, request, session, url_for, redirect
import uuid
import sqlite3
from utils import db_tricks

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def init_db():
    conn = sqlite3.connect('sessions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            candidate TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()



@app.route('/offer', methods=['POST'])
def offer():
    try:
        data = request.get_json()
        print('offer', data)
        session_id = data['session_id']
        print('session_id on offer:', session_id)
        offer_sdp = data['offer']
        print('offer_sdp on offer:', offer_sdp)
        dic = {
            'session_id': str(session_id),
            'offer': json.dumps(offer_sdp),
            'answer': json.dumps(offer_sdp)
        }

        print('dic on offer:', dic)
        db_tricks.change_row(
            db_file='sessions.db',
            db='sessions',
            field='session_id',
            criteria=session_id,
            dic=dic
        )
        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"Exception in offer: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/answer', methods=['POST'])
def answer():
    try:
        data = request.get_json()
        print('answer', data)
        session_id = data['session_id']
        answer_sdp = data['answer']
        conn = sqlite3.connect('sessions.db')
        c = conn.cursor()
        # Inserindo ou atualizando a resposta para esta sessão
        c.execute('''
            INSERT INTO sessions (session_id, answer)
            VALUES (?, ?)
            ON CONFLICT(session_id) DO UPDATE SET answer = ?
        ''', (session_id, answer_sdp, answer_sdp))
        conn.commit()
        conn.close()
        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"Exception in answer: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500



@app.route('/get-offer/<session_id>', methods=['GET'])
def get_offer(session_id):
    try:
        print('get-offer', session_id)
        conn = sqlite3.connect('sessions.db')
        c = conn.cursor()
        c.execute('SELECT offer FROM sessions WHERE session_id = ?', (session_id,))
        row = c.fetchone()
        conn.close()
        if row:
            return jsonify({'offer': row[0]})
        return jsonify({'error': 'Offer not found'}), 404
    except Exception as e:
        print(f"Exception in get_offer: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/get-answer/<session_id>', methods=['GET'])
def get_answer(session_id):
    try:
        print('get-answer', session_id)
        conn = sqlite3.connect('sessions.db')
        c = conn.cursor()
        c.execute('SELECT answer FROM sessions WHERE session_id = ?', (session_id,))
        row = c.fetchone()
        conn.close()
        if row:
            return jsonify({'answer': row[0]})
        return jsonify({'error': 'Answer not found'}), 404
    except Exception as e:
        print(f"Exception in get_answer: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


import json

@app.route('/ice-candidate', methods=['POST'])
def ice_candidate():
    try:
        data = request.get_json()
        print('ice-candidate', data)
        session_id = data['session_id']
        candidate = json.dumps(data['candidate'])  # Serializa o objeto candidate para uma string JSON
        conn = sqlite3.connect('sessions.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO candidates (session_id, candidate)
            VALUES (?, ?)
        ''', (session_id, candidate))
        conn.commit()
        conn.close()
        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"Exception in ice_candidate: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500




@app.route('/get-candidates/<session_id>', methods=['GET'])
def get_candidates(session_id):
    try:
        conn = sqlite3.connect('sessions.db')
        c = conn.cursor()
        c.execute('SELECT candidate FROM candidates WHERE session_id = ?', (session_id,))
        # Aqui, em vez de retornar uma lista de strings JSON,
        # deserializamos cada candidato para um objeto Python e retornamos a lista desses objetos.
        candidates = [json.loads(row[0]) for row in c.fetchall()]
        conn.close()
        if candidates:
            return jsonify({'candidates': candidates})
        return jsonify({'error': 'Candidates not found'}), 404
    except Exception as e:
        print(f"Exception in get_candidates: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/ice-candidate', methods=['POST'])
def save_ice_candidate():
    try:
        data = request.get_json()
        session_id = data['session_id']
        ice_candidate = json.dumps(data['candidate'])

        with sqlite3.connect('sessions.db') as conn:
            c = conn.cursor()
            # Recuperar os candidatos ICE atuais, adicionar o novo e salvar novamente
            c.execute('SELECT ice_candidates FROM signaling WHERE session_id = ?', (session_id,))
            row = c.fetchone()
            candidates = json.loads(row[0]) if row and row[0] else []
            candidates.append(ice_candidate)
            c.execute('''
                UPDATE signaling SET ice_candidates = ? WHERE session_id = ?
            ''', (json.dumps(candidates), session_id))
            conn.commit()

        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"Exception in save_ice_candidate: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/get-sdp/<session_id>', methods=['GET'])
def get_sdp(session_id):
    try:
        with sqlite3.connect('sessions.db') as conn:
            c = conn.cursor()
            c.execute('SELECT offer, answer FROM signaling WHERE session_id = ?', (session_id,))
            row = c.fetchone()

        if row:
            return jsonify({'offer': row[0], 'answer': row[1]})
        else:
            return jsonify({'error': 'Session not found'}), 404
    except Exception as e:
        print(f"Exception in get_sdp: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/get-ice-candidates/<session_id>', methods=['GET'])
def get_ice_candidates(session_id):
    try:
        with sqlite3.connect('sessions.db') as conn:
            c = conn.cursor()
            c.execute('SELECT ice_candidates FROM signaling WHERE session_id = ?', (session_id,))
            row = c.fetchone()

        if row and row[0]:
            return jsonify({'ice_candidates': json.loads(row[0])})
        else:
            return jsonify({'error': 'No ICE candidates found'}), 404
    except Exception as e:
        print(f"Exception in get_ice_candidates: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/request_access', methods=['GET', 'POST'])
def index():
    if 'session_id' in session:
        session_id = session['session_id']
    else:
        session_id = session['session_id'] = uuid.uuid4()
    return render_template('request_access.html', session_id=session_id)


@app.route('/get_available_sessions', methods=['GET', 'POST'])
def get_available_sessions():
    args = request.args if request.args else request.form
    if 'chosen_session' in args:
        session['chosen_session'] = args.get('chosen_session')
        return redirect(url_for('answer_session'))
    else:

        sessions_tuples = db_tricks.fetch_all_col(
            db_file='sessions.db',
            db='sessions',
            field='session_id',
        )

        session_list = [ses[0] for ses in sessions_tuples]

        return render_template('get_available_sessions.html', session_list=session_list)



@app.route('/answer_session', methods=['GET', 'POST'])
def answer_session():
    try:
        args = request.json
    except:
        args = request.args if request.args else request.form
    print('args', args)

    if 'type' in args:
        print('entrou no args')
        return json.dumps(args)
    else:

        ch = db_tricks.search_row(
            db_file='sessions.db',
            db='sessions',
            field='session_id',
            criteria=session['chosen_session']
        )

        chosen_session = ch[0]
        sdp = ch[1]
        print('sdp', sdp)
        return render_template('answer_session.html', chosen_session=chosen_session, sdp=sdp)


@app.route('/waiting_room', methods=['GET', 'POST'])
def waiting_room():  # Função para aguardar aceite de sessão do cliente 2
    ...


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)