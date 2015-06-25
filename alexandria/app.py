# coding=utf-8

from flask import Flask
#from flask import Response
from flask import jsonify
import config


# Vars
alexandria_version="0.1"
    
# Configuration file
conf_file = config.AlexandriaConfiguration('alexandria.conf')

# Initialise Flask
app = Flask(__name__)    
app.debug = True

@app.route('/drivers', methods = ['GET'])
def api_drivers():
    data = {'drivers' : conf_file.get_drivers()}
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/drivers/<driver_name>')
def api_driver(driver_name):
    data = {driver_name : conf_file.get_driver_info(driver_name)}
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/', methods = ['GET'])
def api_root():
    global alexandria_version
    data = {
        'Service'  : 'Alexandria',
        'Version' : alexandria_version
    }

    resp = jsonify(data)
    resp.status_code = 200

    resp.headers['Link'] = 'http://luisrei.com'

    return resp


if __name__ == '__main__':
    app.run()
