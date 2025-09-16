import base64
import subprocess
import re
import ipaddress
import flask

def run_ping(ip_base64):
    try:
        decoded_ip = base64.b64decode(ip_base64).decode('utf-8')
        if not re.match(r'^\d+\.\d+\.\d+\.\d+$', decoded_ip):
            return False
        if decoded_ip.count('.') != 3:
            return False
        
        if not all(0 <= int(part) < 256 for part in decoded_ip.split('.')):
            return False
        if not ipaddress.ip_address(decoded_ip):
            return False
        if len(decoded_ip) > 15:
            return False
        if not re.match(r'^[A-Za-z0-9+/=]+$', ip_base64):
            return False
    except Exception as e:
        return False
    command = f"""echo "ping -c 1 $(echo '{ip_base64}' | base64 -d)" | sh"""

    try:
        process = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        return process.stdout
    except Exception as e:
        return False

app = flask.Flask(__name__)

@app.route('/ping', methods=['POST'])
def ping():
    data = flask.request.json
    ip_base64 = data.get('ip_base64')
    if not ip_base64:
        return flask.jsonify({'error': 'no ip'}), 400

    result = run_ping(ip_base64)
    if result:
        return flask.jsonify({'success': True, 'output': result}), 200
    else:
        return flask.jsonify({'success': False}), 400

@app.route('/')
def index():
    return flask.render_template('index.html')

app.run(host='0.0.0.0', port=5000)