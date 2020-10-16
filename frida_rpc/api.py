import random
from flask import Flask, request, jsonify
from frida_rpc.frida_hook import run, get_serial_ids, client, redis_name

app = Flask(__name__)

@app.route('/index', methods=['GET'])
def index():
    return 'Hello!'


@app.route('/skcy', methods=['POST'])
def get_skcy():
    query = request.get_json(force=True)

    if len(get_serial_ids()) == 0:
        return jsonify({'code': 1, 'msg': {'skcy': None}, 'error': "没有可用的手机"})

    serial_ids = get_serial_ids()
    serial_id = random.choice(list(serial_ids))

    try:
        skcy = run(query['query'], serial_id)
    except Exception as e:
        # client.srem(redis_name, serial_id)
        return jsonify({'code': 1, 'msg': {'skcy': None, 'serial_id': serial_id}, 'error': e.args[0]})

    return jsonify({'code': 0, 'msg': {'skcy': skcy, 'serial_id': serial_id}, 'error': None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
