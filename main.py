from components.args import Args
from components.config import Config
from components.instances_set import InstancesSets
from components.relations_set import  RelationsSets
from components.workflow import Workflow

args = Args()
config = Config(args.workflow)

config.empty_output()

Workflow(config).execute()

config.save_layer("simulation_area", "simulation_area.geojson")
config.save_layer("hospitals", "hospitals.geojson")
config.save_layer("network", "network.geojson")
config.save_layer("emergency_areas", "emergency_areas.geojson")

auto_instances = InstancesSets()
auto_instances.add_set_from_layer(8, config.layer("emergency_areas"), "dauid", ["dauid", "DApop_2016"])
auto_instances.add_set_from_layer(9, config.layer("hospitals"), "index", ["index", "facility_name", "rate", "capacity"])
auto_instances.dump('./output/auto_instances.json')

auto_relations = RelationsSets()
auto_relations.add_set(8, "emergency_area_defs::out_1", 9, "hospital_defs::processor_in")
auto_relations.add_set(8, "emergency_area_defs::out_2", 9, "hospital_defs::processor_in")
auto_relations.add_set(8, "emergency_area_defs::out_3", 9, "hospital_defs::processor_in")
auto_relations.add_set(9, "hospital_defs::processor_out", 8, "emergency_area_defs::rejected_1")
auto_relations.sets[0].fill(config.layer("emergency_areas"), "dauid", "hospitals", lambda src, links: [[src, links[0]]])
auto_relations.sets[1].fill(config.layer("emergency_areas"), "dauid", "hospitals", lambda src, links: [[src, links[1]]])
auto_relations.sets[2].fill(config.layer("emergency_areas"), "dauid", "hospitals", lambda src, links: [[src, links[2]]])
auto_relations.sets[3].fill(config.layer("emergency_areas"), "dauid", "hospitals", lambda src, links: [[lnk_id, src] for lnk_id in links])
auto_relations.dump('./output/auto_relations.json')
