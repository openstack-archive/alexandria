# coding=utf-8

import types
import config


class Driver(object):

    def __init__(self):
        self.driver_type = self.__class__.__name__
        # Get credentials from conf files for CMDB
        pass

    def get_driver_type(self):
            return self.driver_type

    def get_ci(self,ci):
        pass

    def push_ci(self,ci):
        pass


class Itop(Driver):

    def get_ci(self,ci):
        print "Get from itop"
        return True

    def push_ci(self):
        pass

class Redfish(Driver):

    def get_ci(self,ci):
        print "Get from redfish"
        return True

class Ironic(Driver):
    pass

class Mondorescue(Driver):
    pass

class Fakecmdb(Driver):
    pass

class Fakeprovider(Driver):
    
    def get_ci(self,ci):
        import app
        # Simulate a driver that will provide Manager data.
        
        # TODO a connect method must be implemented as 
        
        # Assuming the connection is ok.
        
        # Now create a manager model from reference model.
        ci.ci_type = "Manager"
        ci.data = config.alexandria.model.Manager


class DriverCollection(list):
    pass
