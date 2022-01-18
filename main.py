from components.args import Args
from components.config import Config
from components.instances_set import InstancesSets
from components.relations_set import  RelationsSets
from components.auto_coupled import  AutoCoupled
from components.workflow import Workflow

args = Args()
config = Config(args.workflow)

print('\nCleaning any previous output...')
config.empty_output()

print('\nExecuting spatial analysis workflow at ' + args.workflow + '...')
Workflow(config).execute()

config.save_layer("simulation_area", "simulation_area.geojson")
config.save_layer("hospitals", "hospitals.geojson")
config.save_layer("network", "network.geojson")
config.save_layer("emergency_areas", "emergency_areas.geojson")

auto_instances = InstancesSets()
auto_instances.add_set_from_layer("emergency_area", config.layer("emergency_areas"), "id", ["id", "population"])
auto_instances.add_set_from_layer("hospital", config.layer("hospitals"), "id", ["id", "name", "rate", "capacity"])

auto_relations = RelationsSets()
auto_relations.add_set("emergency_area", "out_1", "hospital", "processor_in")
auto_relations.add_set("emergency_area", "out_2", "hospital", "processor_in")
auto_relations.add_set("emergency_area", "out_3", "hospital", "processor_in")
auto_relations.add_set("hospital", "processor_out", "emergency_area", "rejected_1")

# TODO: The double array in the lambda is awkward, need to review this.
auto_relations.sets[0].fill(config.layer("emergency_areas"), "id", "hospitals", lambda src, links: [[src, links[0]]])
auto_relations.sets[1].fill(config.layer("emergency_areas"), "id", "hospitals", lambda src, links: [[src, links[1]]])
auto_relations.sets[2].fill(config.layer("emergency_areas"), "id", "hospitals", lambda src, links: [[src, links[2]]])
auto_relations.sets[3].fill(config.layer("emergency_areas"), "id", "hospitals", lambda src, links: [[lnk_id, src] for lnk_id in links])

auto_top = AutoCoupled("area_1", "gis_emergencies", auto_instances, auto_relations)

config.save_auto_coupled_cbm(auto_top)