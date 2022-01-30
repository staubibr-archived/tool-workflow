from qgis.core import QgsApplication
from qgis.analysis import QgsNativeAlgorithms
from QNEAT3 import Qneat3Provider

from components.args import Args
from components.config import Config
from components.instances_set import InstancesSets
from components.relations_set import  RelationsSets
from components.auto_coupled import  AutoCoupled
from components.workflow import Workflow
from components import tools

# Initialize QGIS Application
QgsApplication.setPrefixPath("D:/Programs/OSGeo4W64/apps/qgis", True)

qgs = QgsApplication([], False)

QgsApplication.initQgis()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

p = Qneat3Provider.Qneat3Provider()
p.loadAlgorithms()

QgsApplication.processingRegistry().addProvider(p)

args = Args()
json = tools.get_json(args.workflow)
config = Config(json, args.input, args.output)

print('\nCleaning any previous output...')
tools.empty_folder(config.output_folder)

print('\nExecuting spatial analysis workflow at ' + args.workflow + '...')
wf = Workflow(config).execute()

for l in config.output.layers:
    print('Saving layer ' + l.name + ' to ' + config.output_path(l.file))
    tools.save_layer(wf.layer(l.name), config.output_path(l.file))

auto_instances = InstancesSets()

for i in config.output.instances:
    auto_instances.add_set_from_layer(i.model, wf.layer(i.layer), i.id_field, i.properties)

auto_relations = RelationsSets()

for r in config.output.relations:
    s = auto_relations.add_set(r.coupling[0], r.coupling[1], r.coupling[2], r.coupling[3])
    s.fill(wf.layer(r.layer), r.fields[0], r.fields[1])

auto_top = AutoCoupled("area_1", "gis_emergencies", auto_instances, auto_relations)

print('Saving component based modeling (CBM) auto coupled model configuration to ' + config.output_path('auto_coupled.json'))
auto_top.dump_cbm(config.output_path('auto_coupled.json'))

qgs.exitQgis()