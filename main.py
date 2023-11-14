from flask import Flask, render_template, jsonify, request, session, url_for, redirect
import uuid
from utils import db_tricks, date_time_operations
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def clean_sessions_web_rtc():
    db_tricks.delete_table(
        db_file='web_rtc.db',
        db='requests'
    )
    db_tricks.delete_table(
        db_file='web_rtc.db',
        db='accepted'
    )

@app.route('/clean_sessions', methods=['POST', 'GET'])
def clean_sessions():
    clean_sessions_web_rtc()
    return "Sessões limpas"


@app.route('/offer', methods=['POST'])
def offer():
    try:
        try:
            data = request.get_json()
            assert data is not None
        except:
            data = request.args if request.args else request.form
            data = data.to_dict()
        print('offer', data)
        session_id = data['session_id']
        print('session_id on offer:', session_id)
        offer_sdp = data['offer']
        print('offer_sdp on offer:', offer_sdp)
        dic = {
            'session_id': str(session_id),
            'offer': json.dumps(offer_sdp)
        }

        print('dic on offer:', dic)
        db_tricks.change_row(
            db_file='web_rtc.db',
            db='offers',
            field='session_id',
            criteria=session_id,
            dic=dic
        )
        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"Exception in offer: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/get-offer', methods=['POST', 'GET'])
def get_offer():
    try:
        data = request.args if request.args else request.form
        data = data.to_dict()
        print('data on get_offer', data)
        session_id = data['session_id']
        answer = db_tricks.search_row(
            db_file='web_rtc.db',
            db='offers',
            field='session_id',
            criteria=session_id
        )
        if answer is None:
            return '', 204
        else:
            return jsonify({'offer': answer[1]})

    except Exception as e:
        print(f"Exception in get_offer: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/create-answer', methods=['POST'])
def create_answer():
    try:
        args = request.json
    except:
        args = request.args if request.args else request.form

    try:
        print('entrou no args')
        dic = {
            'chosen_session': session['chosen_session'],
            'answer': json.dumps(args)
        }
        db_tricks.change_row(
            db_file='web_rtc.db',
            db='answers',
            field='chosen_session',
            criteria=session['chosen_session'],
            dic=dic
        )
        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"Exception in offer: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/get-answer', methods=['GET', 'POST'])
def get_answer():

    try:
        data = request.args if request.args else request.form
        data = data.to_dict()
        print('get_answer data', data)
        session_id = data['session_id']
        answer = db_tricks.search_row(
            db_file='web_rtc.db',
            db='answers',
            field='session_id',
            criteria=session_id
        )
        if answer is None:
            return '', 204
        else:
            return jsonify({'answer': answer})
    except Exception as e:
        print(f"Exception in offer: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500



@app.route('/request-access', methods=['GET', 'POST'])
def request_access():
    args = request.args if request.args else request.form
    if 'session_id' in session:
        session_id = session['session_id']
    else:
        session_id = session['session_id'] = str(uuid.uuid4())
    if 'action' in args:
        if args.get('action') == 'request':
            dic = {
                'session_id': session_id,
                'timestamp': date_time_operations.now()
            }
            db_tricks.change_row(
                db_file='web_rtc.db',
                db='requests',
                field='session_id',
                criteria=str(session_id),
                dic=dic
            )
            return redirect(url_for('waiting_room'))

    else:
        return render_template('request_access.html', session_id=session_id)



@app.route('/get-available-sessions', methods=['GET', 'POST'])
def get_available_sessions():
    args = request.args if request.args else request.form

    if 'chosen_session' in args:
        session['chosen_session'] = session_id = args.get('chosen_session')
        dic = {
            'idd': 'a',
            'session_id': session_id
        }
        db_tricks.change_row(
            db_file='web_rtc.db',
            db='accepted',
            field='idd',
            criteria='a',
            dic=dic
        )

        return redirect(url_for('doctor_room'))  # answer_session
    else:

        session_list = db_tricks.fetch_entire_table(
            db_file='web_rtc.db',
            db='requests'
        )
        if session_list is None:
            session_list = []

        return render_template('get_available_sessions.html', session_list=session_list)



@app.route('/waiting_room', methods=['GET', 'POST'])
def waiting_room():  # Função para aguardar aceite de sessão do cliente 2

    row = db_tricks.search_row(
        db_file='web_rtc.db',
        db='accepted',
        field='session_id',
        criteria=session['session_id']
    )
    if row is None:
        return render_template('waiting_room.html')
    else:
        return redirect(url_for('access_doctor_room'))


@app.route('/doctor_room', methods=['GET', 'POST'])
def doctor_room():  # Função o médico aguardar o paciente
    session_id = session['chosen_session']
    return render_template('doctor_room.html', session_id=session_id)


@app.route('/access_doctor_room', methods=['GET', 'POST'])
def access_doctor_room():
    session_id = session['session_id']
    return render_template('access_doctor_room.html', session_id=session_id)




@app.route('/ice-candidate', methods=['POST'])
def ice_candidate():
    try:
        try:
            data = request.get_json()
            assert data is not None

        except:
            data = request.args if request.args else request.form
            data = data.to_dict()
        session_id = data['session_id']
        candidate = json.dumps(data['candidate'])  # Serializa o objeto candidate para uma string JSON

        num_rows = db_tricks.calculate_table_size(
            db_file='web_rtc.db',
            db='client_ice_candidates'
        )

        if num_rows is None or num_rows == '':
            idd = 1
        else:
            idd = int(num_rows) + 1

        dic = {
            'id': idd,
            'session_id': session_id,
            'candidate': candidate
        }

        db_tricks.add_entry(
            db_file='web_rtc.db',
            db='client_ice_candidates',
            dic=dic
        )

        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"Exception in ice_candidate: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/ice-candidate-doctor', methods=['POST'])
def ice_candidate_doctor():
    try:
        try:
            data = request.get_json()
            assert data is not None
        except:
            data = request.args if request.args else request.form
            data = data.to_dict()
        session_id = data['session_id']
        candidate = json.dumps(data['candidate'])  # Serializa o objeto candidate para uma string JSON

        num_rows = db_tricks.calculate_table_size(
            db_file='web_rtc.db',
            db='doctor_ice_candidates'
        )

        if num_rows is None or num_rows == '':
            idd = 1
        else:
            idd = num_rows + 1

        dic = {
            'id': idd,
            'session_id': session_id,
            'candidate': candidate
        }

        db_tricks.add_entry(
            db_file='web_rtc.db',
            db='doctor_ice_candidates',
            dic=dic
        )

        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"Exception in ice_candidate_doctor: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/get-ice-candidate-from-doctor', methods=['GET', 'POST'])
def get_ice_candidates_from_doctor():
    session_id = request.args.get('session_id')

    candidates = db_tricks.search_entire_db(
        db_file='web_rtc.db',
        db='doctor_ice_candidates',
        field='session_id',
        criteria=session_id
    )
    if candidates is None:
        return '', 204
    else:
        candidate_list = list(candidates)

        return jsonify(candidate_list)

@app.route('/get-ice-candidate-from-client', methods=['GET', 'POST'])
def get_ice_candidates_from_client():
    session_id = request.args.get('session_id')

    print('session_id on get_ice_candidates_from_client', session_id)

    candidates = db_tricks.search_entire_db(
        db_file='web_rtc.db',
        db='client_ice_candidates',
        field='session_id',
        criteria=session_id
    )
    if candidates is None:
        return '', 204

    else:
        candidate_list = list(candidates)

        return jsonify(candidate_list)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
