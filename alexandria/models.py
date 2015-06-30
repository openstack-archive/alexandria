# coding=utf-8

import json
import glob
import os
import re

class Model(object):
    """Implements Alexandria reference model."""
    def __init__(self):
        
        self.reference_items = []
        
        self.read_ref_files()
        pass
    
    
    def read_ref_files(self):
        cwd = os.getcwd()
        model_files = glob.glob(cwd + "/model/*.json")     
        
        for file in model_files:
            # Derive attribute name from file.
            attr_name = os.path.basename(file)
            attr_name = re.sub(r"\..*$", "", attr_name)
            
            # read json file
            with open(file) as json_data:
                data_structure = json.load(json_data)
                json_data.close()
    
            # Create an class attribute for that structure
            setattr(self, attr_name, data_structure)
            self.reference_items.append(attr_name)
        return True
        
        