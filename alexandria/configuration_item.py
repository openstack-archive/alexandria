# coding=utf-8



class ConfigurationItem(object):
    
    def __init__(self,uuid,ip_mgmt,login,password):
        
        self.uuid = uuid
        self.ip_mgmt = ip_mgmt
        self.login = login
        self.password = password
               
        self.ci_parents = [] # List to store parents ci
        self.ci_children = [] # List to store children ci
        
    @property
    def ci_type(self):
        return self.__ci_type
        
    @ci_type.setter
    def ci_type(self, ci_type):
        self.__ci_type = ci_type
        
    @property
    def data(self):
        return self.__data
        
    @data.setter
    def data(self, data):
        self.__data = data
        
        

