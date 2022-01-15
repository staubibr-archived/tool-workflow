
from components.workflow import Workflow

class WFEmergencyAreas(Workflow):

    def __init__(self, workflow_file):
        super().__init__(workflow_file)

    def execute(self):
        self.log_wf('PROCESSING DA LAYER AS EMERGENCY AREAS')
        self.log_step('Clip (Extract DAs within the simulation area.')
        result = self.execute_task("native:clip", {
            'INPUT': self.config.layer("DA"),
            'OUTPUT': "TEMPORARY_OUTPUT",
            'OVERLAY': self.config.layer("simulation_area")
        })

        self.log_step('Delete Columns (Remove unused columns from emergency areas.')
        result = self.execute_task("native:deletecolumn", {
            'INPUT': result,
            'COLUMN': ['fid', 'id', 'pruid', 'prname', 'cduid', 'cdname', 'cdtype', 'ccsuid', 'ccsname', 'csduid',
                       'csdname', 'csdtype', 'eruid', 'ername', 'saccode', 'sactype', 'cmauid', 'cmapuid', 'cmaname',
                       'cmatype', 'ctuid', 'ctname', 'adauid'],
            'OUTPUT': "TEMPORARY_OUTPUT",
        })

        self.log_step('Reproject Layer (Reproject emergency areas to 4326 for QNEAT3.')
        result = self.execute_task("native:reprojectlayer", {
            'INPUT': result,
            'OUTPUT': "TEMPORARY_OUTPUT",
            'TARGET_CRS': self.crs
        })

        self.log_step('Join Attributes Table (Join population counts on emergency areas.')
        result = self.execute_task("native:joinattributestable", {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'dauid',
            'FIELDS_TO_COPY': ['DApop_2016'],
            'FIELD_2': 'DAuid',
            'INPUT': result,
            'INPUT_2': self.config.data('DA_pop'),
            'METHOD': 1,
            'OUTPUT': "TEMPORARY_OUTPUT",
            'PREFIX': ''
        })

        self.log_step('Refactor Fields (DA_pop is string because CSV, convert to int.')
        return self.execute_task("native:refactorfields", {
            'FIELDS_MAPPING': [{'expression': '\"dauid\"', 'length': 0, 'name': 'dauid', 'precision': 0, 'type': 10},
                               {'expression': '\"DApop_2016\"', 'length': 0, 'name': 'DApop_2016', 'precision': 0,
                                'type': 2}],
            'INPUT': result,
            'OUTPUT': "TEMPORARY_OUTPUT",
        })