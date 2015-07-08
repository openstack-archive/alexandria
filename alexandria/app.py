# coding=utf-8

from flask import Flask
from flask import jsonify
from flask import request
import sys
import pprint
import logging
from logging.handlers import RotatingFileHandler
import config
import models
import configuration_item
import drivers


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
    data = {"drivers" : conf_file.get_drivers()}
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route("/drivers/<driver_name>")
def api_driver(driver_name):
    data = {driver_name : conf_file.get_driver_info(driver_name)}
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
    
    #driver_list = conf_file.get_drivers()
    
    #for driver in driver_list:
        #driver.get(ci)
    pp.pprint(alexandria_cis)
    
    app.logger.debug("Debug message")
    
    return ("ok")

@app.route('/ci', methods=['PUT'])
def update_ci():
    pass

@app.route("/", methods = ["GET"])
def api_root():
    
    #global alexandria
    data = {
        "Service"  : "Alexandria",
        "Version" : alexandria.version
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


class Alexandria(object):
    def __init__(self):
        self.version = "0.1"
        
        # Model
        self.model = models.Model()
        
        # Configuration file
        self.conf_file = config.AlexandriaConfiguration("alexandria.conf")

        # Build driver list from configuration file
        driver_name_list = self.conf_file.get_drivers()
        
        self.drivers = drivers.DriverCollection()    

        # Create objects !!!! TO BE CONTINUED !!!!
        for driver_name in driver_name_list:
            # Get class
            driver_class = getattr(sys.modules["drivers"], driver_name.capitalize())
            # Create object
            driver_object = driver_class()
            # Add to driver list
            self.drivers.append(driver_object) 
            index = self.drivers.index(driver_object)
            # Set an attribute to the coresponding driver
            setattr(self.drivers, driver_name.lower(), self.drivers[index])                      


if __name__ == "__main__":
    # Vars
    app_logfile = "/var/log/alexandria/alexandria.log"
      
    global alexandria

    alexandria = Alexandria()
    
    # Define a PrettyPrinter for debugging.
    pp = pprint.PrettyPrinter(indent=4)
      
    # Define a structure to handle ci
    alexandria_cis = {}
    
    # Configure Flask logger
    configure_logger(app.logger, app_logfile)
    
    
    # Debugging stuff to remove later.
    print alexandria.model.reference_items
    print alexandria.drivers.itop.get()
    print alexandria.drivers.redfish.get()
    print alexandria.drivers.itop.driver_type
    #pp.pprint(models.EthernetInterface)  # debugging example.
    #pp.pprint(models.Manager)  # debugging example.
    app.logger.info("Starting Alexandria...")
    app.run(port=int(alexandria.conf_file.get_alexandria_port()))
    
    
    