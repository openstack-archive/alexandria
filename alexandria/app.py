# coding=utf-8

import pprint
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask import jsonify
from flask import request
import config
import configuration_item


# Initialise Flask
app = Flask(__name__)
app.debug = True


@app.route("/drivers", methods = ["GET"])
def api_drivers():
    """Return drivers.

    :param nome
    :type na
    :returns:  http response

    """
    data = {"drivers" : config.alexandria.conf_file.get_drivers()}
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route("/drivers/<driver_name>")
def api_driver(driver_name):
    data = {driver_name : config.alexandria.conf_file.get_driver_info(driver_name)}
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    app.logger.info("Stopping Alexandria...")
    return 'Server shutting down...'

@app.route('/bruno', methods=['POST'])
def bruno():
    coucou = "Coucou " + request.json["Server"]
    #coucou = "Coucou"
    return coucou

@app.route('/ci', methods=['POST'])
def create_ci():
    pp = pprint.PrettyPrinter(indent=4)
    
    ci = configuration_item.ConfigurationItem(request.json["uuid"],
                              request.json["ip_mgmt"],
                              request.json["login"],
                              request.json["password"])
    
    # TODO : Error case uuid already available
    #        Uuid malformed 
    #        Generate a random uuid (check uuid module) if uuid = None
    
    alexandria_cis.update({request.json["uuid"]: ci })
    
    # Synchronize data beetween all our drivers
    synchronize_ci(ci)
    
    app.logger.debug("citype {}".format(ci.ci_type))
    
    # TODO : Remove next line, used just for debugging...
    pp.pprint(alexandria_cis)
    
    app.logger.debug("Debug message")
    
    # Craft response
    resp = jsonify(ci.data)
    resp.status_code = 200
    
    resp.headers["AuthorSite"] = "https://github.com/uggla/alexandria"

    return resp
    
def synchronize_ci(ci):
    # Now do a "broadcast" get to all our drivers 
    for driver in config.alexandria.drivers:
        app.logger.info("Get information from {} driver.".format(driver.get_driver_type()))
        driver.get_ci(ci)
        
    # Push the data provided above to all our drivers
    for driver in config.alexandria.drivers:
        app.logger.info("Push information to {} driver.".format(driver.get_driver_type()))
        driver.push_ci(ci)
    

@app.route('/ci', methods=['PUT'])
def update_ci():
    pass

@app.route("/", methods = ["GET"])
def api_root():
    data = {
        "Service"  : config.alexandria.name,
        "Version" : config.alexandria.version
    }

    resp = jsonify(data)
    resp.status_code = 200

    resp.headers["AuthorSite"] = "https://github.com/uggla/alexandria"

    return resp

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def configure_logger(logger,logfile): 
    
    formatter = logging.Formatter(
        '%(asctime)s :: %(levelname)s :: %(message)s'
        )
    file_handler = RotatingFileHandler(logfile, 'a', 1000000, 1)

    # Add logger to file
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


if __name__ == "__main__":
    # Vars
    app_logfile = "/var/log/alexandria/alexandria.log"
    
    # Define a PrettyPrinter for debugging.
    pp = pprint.PrettyPrinter(indent=4)
      
    # Define a structure to handle ci
    alexandria_cis = {}
    
    # Configure Flask logger
    configure_logger(app.logger, app_logfile)
    
    
    # TODO : Debugging stuff to remove later.
    print config.alexandria.model.reference_items
    print config.alexandria.drivers.itop.get_ci(None)
    print config.alexandria.drivers.redfish.get_ci(None)
    print config.alexandria.drivers.itop.driver_type
    #pp.pprint(models.EthernetInterface)  # debugging example.
    #pp.pprint(models.Manager)  # debugging example.
    app.logger.info("Starting Alexandria...")
    app.run(port=int(config.alexandria.conf_file.get_alexandria_port()))
    
    
    