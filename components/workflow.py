from qgis.core import QgsApplication, QgsCoordinateReferenceSystem
from qgis.analysis import QgsNativeAlgorithms
from QNEAT3 import Qneat3Provider
import processing

# Prepare QGIS environment
from tasks import tsk_closest

QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

p = Qneat3Provider.Qneat3Provider()
p.loadAlgorithms()

QgsApplication.processingRegistry().addProvider(p)

class Workflow:
    N = 0

    CUSTOM= {
        "custom:closest": tsk_closest
    }

    def __init__(self, config):
        self.config = config
        self.previous = None

        self.crs = QgsCoordinateReferenceSystem("epsg:4326")

    # noinspection PyMethodMayBeStatic
    def execute_task(self, name, params):
        if name in Workflow.CUSTOM:
            return Workflow.CUSTOM[name].auto_execute(params)

        result = processing.run(name, params)

        return result["OUTPUT"]

    def execute_task_json(self, task):
        name = task["name"]
        params = task["params"]

        Workflow.N += 1

        print("\n\t" + str(Workflow.N) + ". Running " + name + "...")
        print("\t" + "{0}".format(params) + "...")

        for key in params:
            if key == "TARGET_CRS":
                params[key] = QgsCoordinateReferenceSystem("epsg:" + params[key])

            elif not isinstance(params[key], dict) or not "type" in params[key]:
                continue

            elif "name" in params[key]:
                params[key] = self.config.get(params[key]["type"], params[key]["name"])

            elif "names" in params[key]:
                params[key] = [self.config.get(params[key]["type"], name) for name in params[key]["names"]]

            elif params[key]["type"] == "result":
                params[key] = self.previous

        self.previous = self.execute_task(name, params)

        if "output" in task:
            self.config.add_layer(task["output"], self.previous)

        return self.previous

    def execute(self):
        for task in self.config.tasks:
            self.execute_task_json(task)

        print('\nWorkflow executed successfully.')

    # noinspection PyMethodMayBeStatic
    def log_wf(self, message):
        print('\n*** ' + message + ' ***')

