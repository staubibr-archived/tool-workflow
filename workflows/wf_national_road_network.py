
from components.workflow import Workflow

class WFNationalRoadNetwork(Workflow):

    def __init__(self, workflow_file):
        super().__init__(workflow_file)

    def execute(self):
        self.log_wf('PROCESSING NATIONAL ROAD NETWORK')
        self.log_step('Clip (Extract QC NRN for simulation area.')
        result_1 = self.execute_task("native:clip", {
            'INPUT': self.config.layer('NRN_QC'),
            'OVERLAY': self.config.layer('simulation_area'),
            'OUTPUT': "TEMPORARY_OUTPUT"
        })

        self.log_step('Clip (Extract ON NRN for simulation area.')
        result_2 = self.execute_task("native:clip", {
            'INPUT': self.config.layer('NRN_ON'),
            'OVERLAY': self.config.layer('simulation_area'),
            'OUTPUT': "TEMPORARY_OUTPUT"
        })

        self.log_step('Merge Vector Layers (Merge ON and QC NRN together.')
        result = self.execute_task("native:mergevectorlayers", {
            'LAYERS': [result_1, result_2],
            'OUTPUT': 'TEMPORARY_OUTPUT'
        })

        self.log_step('Reproject Layer (Reproject network to 4326 for QNEAT3.')
        return self.execute_task("native:reprojectlayer", {
            'INPUT': result,
            'OUTPUT': "TEMPORARY_OUTPUT",
            'TARGET_CRS': self.crs
        })
