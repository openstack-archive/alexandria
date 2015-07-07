# coding=utf-8

class Driver(object):
    
    def __init__(self):
        # Get credentials from conf files for CMDB       
        pass

class Itop(Driver):
    
    def get(self):
        print "Get from itop"
        return True

    
    def push(self):
        pass

class Redfish(Driver):
    pass

class Ironic(Driver):
    pass

class Mondorescue(Driver):
    pass

class Fakecmdb(Driver):
    pass

class Fakeprovider(Driver):
    pass


