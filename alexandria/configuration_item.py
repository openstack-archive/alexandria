# coding=utf-8



class ConfigurationItem(object):
    
    def __init__(self,uuid,ip_mgmt,login,password):
        
        self.uuid = uuid
        self.ip_mgmt = ip_mgmt
        self.login = login
        self.password = password
        
        self.ci_type = None
        self.__data = None
        
        
