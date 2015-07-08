# coding=utf-8

import types

class Driver(object):
    
    def __init__(self):
        self.driver_type = self.__class__.__name__
        # Get credentials from conf files for CMDB       
        pass
    
    def get_ci(self):
        pass
    
    def push_ci(self):
        pass


class Itop(Driver):
    
    def get_ci(self):
        print "Get from itop"
        return True
    
    def push_ci(self):
        pass

class Redfish(Driver):
    
    def get_ci(self):
        print "Get from redfish"
        return True
    
    pass

class Ironic(Driver):
    pass

class Mondorescue(Driver):
    pass

class Fakecmdb(Driver):
    pass

class Fakeprovider(Driver):
    pass


class DriverCollection(list):
    pass

    