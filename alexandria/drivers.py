# coding=utf-8

import pprint
import config
import json
import urllib
import requests


class Driver(object):

    def __init__(self):
        self.driver_type = self.__class__.__name__
        # Get credentials from conf files for CMDB
        pass

    def get_driver_type(self):
            return self.driver_type

    def get_ci(self, ci):
        pass

    def set_ci(self, ci):
        pass


class Itop(Driver):

    def get_ci(self, ci):
        print("Get from itop")
        return True

    def set_ci(self, ci):
        username = config.alexandria.conf_file.get_driver_parameters("itop", "loginItop")
        password = config.alexandria.conf_file.get_driver_parameters("itop", "passwordItop")
        config.logger.debug("login : {}, password : {}".format(
                                                               username,
                                                               password
                                                               )
                            )
        # Craft request body and header
        urlbase = config.alexandria.conf_file.get_driver_parameters("itop", "endpoint")
        
              
        request = '{"operation":"core/create","comment":"Synchronization from Alexandria","class":"Server","output_fields":"id,name,ram", "fields":{"org_id": "3","name":"' + ci.data["Name"] + '","ram":"' + format((ci.data["MemorySummary"])["TotalSystemMemoryGiB"]) + '","serialnumber":"' + ci.data["SerialNumber"] + '"}}'
        
        urlparam = {'version' : '1.0',
                    'auth_user' : username,
                    'auth_pwd' : password,
                    'json_data' : request
                    }
        
        #header = {'Content-type': 'application/json'}
        
        url = urlbase + '?' + urllib.urlencode(urlparam)
        
        config.logger.debug(url)
        
        #=======================================================================
        # answer = requests.post(url,
        #                      headers=header,
        #                      verify="False"
        #                     )
        #=======================================================================
        answer = requests.post(url,
                               auth=(username,password)
                              )
        
        config.logger.debug(answer.status_code)
        config.logger.debug(answer.text)


class Redfish(Driver):

    def get_ci(self,ci):
        print("Get from redfish")
        import redfish
        
        print(ci.ip_mgmt + " - " + ci.login + " - " + ci.password)
        
        #remote_mgmt = redfish.connect(ci.ip_mgmt, ci.login, ci.password, verify_cert=False)
        remote_mgmt = redfish.connect(ci.ip_mgmt, ci.login, ci.password, simulator=True, enforceSSL=False)
                                       
        ci.ci_type = remote_mgmt.Systems.systems_list[0].get_parameter("@odata.type")
        ci.data = remote_mgmt.Systems.systems_list[0].get_parameters()
                
        #print("Redfish API version : {} \n".format(remote_mgmt.get_api_version()))       
        return True

    def set_ci(self, ci):
        print "Push to Redfish"
        return True

class Ironic(Driver):
    pass


class Mondorescue(Driver):
    pass


class Fakecmdb(Driver):
    def set_ci(self, ci):
        # Determine ci type so we can do the proper action.
        pp = pprint.PrettyPrinter(indent=4)
        if ci.ci_type == "Manager":
            print("We are in Fakecmdb driver !")
            pp.pprint(ci.data)
            # Simply write a json file with ci.data content.
            with open("Fakecmdb.json", "w") as jsonfile:
                json.dump(ci.data, jsonfile, indent=4)
            jsonfile.close()

        #
        #=======================================================================

class Fakeprovider(Driver):

    def get_ci(self, ci):
        # Simulate a driver that will provide Manager data.

        # TODO a connect method must be implemented

        # Assuming the connection is ok.

        # Now create a copy of manager model from reference model.
        #ci.ci_type = "Manager"
        #ci.data = config.alexandria.model.get_model("Manager")

        # Update the structure with data
        # TODO : think to encapsulate to not edit ci.data directly.
        #        This could be also a way to check source of truth.
        #        If data provided by our driver is not the source of truth
        #        then discard it.


        #ci.data["ManagerType"] = "BMC"
        #ci.data["Model"] = "Néné Manager"
        #ci.data["FirmwareVersion"] = "1.00"




        #if ci.data is config.alexandria.model.Manager:
        #    print "identical"

        pp = pprint.PrettyPrinter(indent=4)

        pp.pprint(ci.ci_type)


class DriverCollection(list):
    pass
