
from components.workflow import Workflow

import tasks.tsk_closest as tsk_closest

class WFDistanceMatrix(Workflow):

    def __init__(self, workflow_file):
        super().__init__(workflow_file)

    def execute(self):
        self.log_wf('GENERATING ORIGIN DESTINATION MATRIX')
        self.log_step('Centroids (Generating centroids for emergency areas.')
        result = self.execute_task("native:centroids", {
            'ALL_PARTS': False,
            'INPUT': self.config.layer("emergency_areas"),
            'OUTPUT': "TEMPORARY_OUTPUT"
        })

        self.log_step('Origin Destination Matrix From Layers As Table (Origin destination matrix between emergency areas and hospitals.')
        result = self.execute_task("qneat3:OdMatrixFromLayersAsTable", {
            'DEFAULT_DIRECTION': 2,
            'DEFAULT_SPEED': 55,
            'DIRECTION_FIELD': '',
            'ENTRY_COST_CALCULATION_METHOD': 0,
            'FROM_ID_FIELD': 'dauid',
            'FROM_POINT_LAYER': result,
            'INPUT': self.config.layer("network"),
            'OUTPUT': "TEMPORARY_OUTPUT",
            'SPEED_FIELD': '',
            'STRATEGY': 0,
            'TOLERANCE': 0,
            'TO_ID_FIELD': 'index',
            'TO_POINT_LAYER': self.config.layer("hospitals"),
            'VALUE_BACKWARD': '',
            'VALUE_BOTH': '',
            'VALUE_FORWARD': ''
        })

        self.log_step('Determining 3 closest hospitals to each emergency area from OD matrix.')
        return tsk_closest.execute(result, self.config.layer("emergency_areas"), 'dauid', 'hospitals', 3)