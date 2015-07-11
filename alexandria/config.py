# coding=utf-8

import sys
import ConfigParser
import models
import drivers

# Initialise global variable
logger = None
alexandria = None

def initialise_alexandria():
    """Define alexandria global object so it can be called from anywhere."""
    global alexandria
    # TODO : at a protection to not initialise twice.
    alexandria = Alexandria()

class Alexandria(object):
    def __init__(self):
        self.NAME = "Alexandria"
        self.VERSION = "0.1"
        
        # Model
        self.model = models.Model()
        
        # Configuration file
        self.conf_file = AlexandriaConfiguration("alexandria.conf")

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


class AlexandriaConfiguration(object):

    def __init__(self, configuration_file):
        self.config = ConfigParser.ConfigParser(allow_no_value=True)
        self.config.read(configuration_file)

    def get_drivers(self):
        drivers = self.config.sections()
        drivers.remove("alexandria")
        return drivers

    def get_driver_info(self,driver):
        return self.config.options(driver)

    def get_alexandria_port(self):
        return self.config.get("alexandria", "port")
