# coding=utf-8

import types
import pprint
import config
import json


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

    def push_ci(self,ci):
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
    def push_ci(self, ci):    
        # Determine ci type so we can do the proper action.
        pp = pprint.PrettyPrinter(indent=4)       
        if ci.ci_type == "Manager":
            print "We are in Fakecmdb driver !"
            pp.pprint(ci.data)
            # Simply write a json file with ci.data content.
            with open("Fakecmdb.json", "w") as jsonfile:
                json.dump(ci.data, jsonfile, indent=4)
            jsonfile.close()

        #     
        #=======================================================================

class Fakeprovider(Driver):
    
    def get_ci(self,ci):
        # Simulate a driver that will provide Manager data.
        
        # TODO a connect method must be implemented
        
        # Assuming the connection is ok.
        
        # Now create a copy of manager model from reference model.
        ci.ci_type = "Manager"
        ci.data = config.alexandria.model.get_model("Manager")
        
        # Update the structure with data
        ci.data["ManagerType"] = "BMC"
        ci.data["Model"] = "Néné Manager"
        ci.data["FirmwareVersion"] = "1.00"
        

        #if ci.data is config.alexandria.model.Manager:
        #    print "identical"

        pp = pprint.PrettyPrinter(indent=4)
        
        pp.pprint(ci.ci_type)


class DriverCollection(list):
    pass
