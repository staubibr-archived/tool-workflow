from qgis.core import QgsCoordinateReferenceSystem, QgsVectorLayer
import processing

# Prepare QGIS environment
from tasks import tsk_closest, tsk_update

class Workflow:
    N = 0

    CUSTOM= {
        "custom:closest": tsk_closest,
        "custom:update": tsk_update
    }

    def __init__(self, config):
        self.config = config
        self.previous = None
        self.layers = {}

        for key in config.input.layers:
            self.layers[key] = QgsVectorLayer(config.input_layer(key))

        self.crs = QgsCoordinateReferenceSystem("epsg:4326")

    # noinspection PyMethodMayBeStatic
    def execute_task(self, name, params):
        if name in Workflow.CUSTOM:
            return Workflow.CUSTOM[name].auto_execute(params)

        if "OUTPUT" not in params:
            params["OUTPUT"] = "TEMPORARY_OUTPUT"

        result = processing.run(name, params)

        return result["OUTPUT"]

    def execute_task_json(self, task):
        Workflow.N += 1

        print("\n\t" + str(Workflow.N) + ". Running " + task.name + "...")
        print("\t" + "{0}".format(task.params) + "...")

        for key in task.params:
            if key == "TARGET_CRS":
                task.params[key] = QgsCoordinateReferenceSystem("epsg:" + task.params[key])

            elif not isinstance(task.params[key], dict) or not "type" in task.params[key]:
                continue

            elif "name" in task.params[key]:
                task.params[key] = self.get(task.params[key]["type"], task.params[key]["name"])

            elif "names" in task.params[key]:
                task.params[key] = [self.get(task.params[key]["type"], name) for name in task.params[key]["names"]]

            elif task.params[key]["type"] == "result":
                task.params[key] = self.previous

        self.previous = self.execute_task(task.name, task.params)

        if task.output is not None:
            self.add_layer(task.output, self.previous)

        return self.previous

    def execute(self):
        for task in self.config.tasks:
            self.execute_task_json(task)

        print('\nWorkflow executed successfully.')

        return self

    def layer(self, name):
        if name not in self.layers:
            raise Exception('Layer {name} is undefined in workflow layers.'.format(name=name))

        return self.layers[name]

    def add_layer(self, name, layer):
        if name in self.layers:
            raise Exception('Layer {name} already exists in config layers.'.format(name=name))

        self.layers[name] = layer

    def get(self, type, name):
        if type == "data":
            return self.config.input_data(name)

        if type == "layers":
            return self.layer(name)

        if type == "parameters":
            return self.config.input.param(name)

        raise Exception('Section {name} is undefined in config.'.format(name=name))
