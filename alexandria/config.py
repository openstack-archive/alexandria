# coding=utf-8

import ConfigParser


class AlexandriaConfiguration(object):
    
    def __init__(self, configuration_file):
        self.config = ConfigParser.ConfigParser(allow_no_value=True)
        self.config.read(configuration_file)
        
    def get_drivers(self):
        return self.config.sections()
    
    def get_driver_info(self,driver):
        return self.config.options(driver)