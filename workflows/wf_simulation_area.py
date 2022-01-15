
from components.workflow import Workflow

class WFSimulationArea(Workflow):

    def __init__(self, workflow_file):
        super().__init__(workflow_file)

    def execute(self):
        self.log_wf('PROCESSING CSD LAYER AS SIMULATION AREA')
        self.log_step('Extract By Expression (Extract multiple polygons for simulation area.')
        result = self.execute_task("native:extractbyexpression", {
            'INPUT': self.config.layer("CSD"),
            'EXPRESSION': "\"csduid\" IN (2482030,2481017,2482025,2482020,2482005,2482015)",
            'OUTPUT': "TEMPORARY_OUTPUT"
        })

        self.log_step('Dissolve (Merge simulation area polygons into a single polygon.')
        result = self.execute_task("native:dissolve", {
            'INPUT': result,
            'OUTPUT': "TEMPORARY_OUTPUT"
        })

        self.log_step('Delete Columns (Remove unused columns from simulation area.')
        return self.execute_task("native:deletecolumn", {
            'INPUT': result,
            'COLUMN': ['fid', 'id', 'csduid', 'csdname', 'csdtype', 'pruid', 'prname', 'cduid', 'cdname', 'cdtype',
                       'ccsuid', 'ccsname', 'eruid', 'ername', 'saccode', 'sactype', 'cmauid', 'cmapuid', 'cmaname',
                       'cmatype'],
            'OUTPUT': "TEMPORARY_OUTPUT"
        })