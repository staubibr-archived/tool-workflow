
from components.workflow import Workflow

class WFHospitals(Workflow):

    def __init__(self, workflow_file):
        super().__init__(workflow_file)

    def execute(self):
        self.log_wf('PROCESSING ODHF LAYER AS HOSPITALS')
        self.log_step('Extract by attribute (Extract hospitals from the ODHF.')
        result = self.execute_task("native:extractbyexpression", {
            'EXPRESSION': '"odhf_facility_type" = \'Hospitals\'',
            'INPUT': self.config.layer("ODHF"),
            'OUTPUT': "TEMPORARY_OUTPUT"
        })

        self.log_step('Extract by attribute (Eliminate bad data from ODHF.')
        result = self.execute_task("native:extractbyexpression", {
            'EXPRESSION': "index IN ('S1245', 'S1290', 'S647')",
            'INPUT': result,
            'OUTPUT': "TEMPORARY_OUTPUT"
        })

        self.log_step('Delete Columns (Remove unused columns from hospitals.')
        result = self.execute_task("native:deletecolumn", {
            'INPUT': result,
            'COLUMN': ["source_facility_type", "odhf_facility_type", "provider", "unit", "street_no", "street_name",
                       "postal_code", "city", "province", "source_format_str_address", "CSDname", "CSDuid", "Pruid",
                       "latitude", "longitude"],
            'OUTPUT': "TEMPORARY_OUTPUT"
        })

        self.log_step('Extract by Location (Extract Hospitals within the simulation area.')
        result = self.execute_task("native:extractbylocation", {
            'INPUT': result,
            'INTERSECT': self.config.layer("simulation_area"),
            'OUTPUT': "TEMPORARY_OUTPUT",
            'PREDICATE': [6]
        })

        self.log_step('Reproject Layer (Reproject hospitals to 4326 for QNEAT3.')
        return self.execute_task("native:reprojectlayer", {
            'INPUT': result,
            'OUTPUT': "TEMPORARY_OUTPUT",
            'TARGET_CRS': self.crs
        })