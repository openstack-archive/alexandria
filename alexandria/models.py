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
        # Hierarchy model/std/*.json
        model_files = glob.glob(cwd + "/model/redfish/*.json")
        for file in model_files:
            print("Loading model file : {}".format(file))
            # Derive attribute name from file.
            attr_name = os.path.basename(file)
            attr_name = re.sub(r"\..*$", "", attr_name)
            attr_name = "__" + attr_name # Make it private 
            
            # read json file
            with open(file) as json_data:
                data_structure = json.load(json_data)
                json_data.close()

            # Create an class attribute for that structure
            setattr(self, attr_name, data_structure)
            self.reference_items.append(attr_name)
        return True

    def get_model(self,model_name):
        if not model_name[0:1] == "__":
            model_name = "__" + model_name
        model = getattr(self, model_name)
        return model.copy()
        
        