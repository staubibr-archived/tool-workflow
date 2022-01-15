from qgis.core import QgsVectorLayer
import json

from components import tools


class Config:
    @property
    def output_folder(self):
        return self.json["output"]

    @property
    def tasks(self):
        return self.json["tasks"]

    def __init__(self, workflow_file):
        self.json = json.load(open(workflow_file))

        for key in self.json["layers"]:
            self.json["layers"][key] = QgsVectorLayer(self.json["layers"][key])

    def output_path(self, name):
        return self.output_folder + "/" + name

    def data(self, name):
        if name not in self.json["data"]:
            raise Exception('Dataset {name} is undefined in config data.'.format(name=name))

        return self.json["data"][name]

    def layer(self, name):
        if name not in self.json["layers"]:
            raise Exception('Layer {name} is undefined in config layers.'.format(name=name))

        return self.json["layers"][name]

    def add_layer(self, name, layer):
        if name in self.json["layers"]:
            raise Exception('Layer {name} already exists in config layers.'.format(name=name))

        self.json["layers"][name] = layer

    def param(self, name):
        if name not in self.json["parameters"]:
            raise Exception('Parameter {name} is undefined in config parameters.'.format(name=name))

        return self.json["parameters"][name]

    def get(self, type, name):
        if type not in self.json:
            raise Exception('Section {name} is undefined in config.'.format(name=name))

        if type == "data":
            return self.data(name)

        if type == "layers":
            return self.layer(name)

        if type == "parameters":
            return self.param(name)

    def save_layer(self, layer_id, file):
        tools.save_layer(self.layer(layer_id), self.output_path(file))

    def empty_output(self):
        tools.empty_folder(self.output_folder)


# config = {
#    "name": "Gatineau",
#    "area": "CSD",
#    "expression": '"csduid" IN (2482030,2481017,2482025,2482020,2482005,2482015)',
#    "hospitals": "index IN ('S1245', 'S1290', 'S647')"
# }

# config = {
#     "name": "Ottawa-Gatineau",
#     "area": "CSD",
#     "expression": '"csduid" IN (3506008,2482030,2481017,2482025,2482020,2482005,2482015)',
#     "hospitals": "index IN ('3968', '4860', '5657', '5658', '5660', 'S1245', 'S1290', 'S647')"
# }

# config = {
#     "name": "Ottawa",
#     "area": "CSD",
#     "expression": '"csduid" IN (3506008)',
#     "hospitals": "index IN ('3968', '4860', '5657', '5658', '5660')"
# }
