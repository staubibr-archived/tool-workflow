from components.tools import *


# START OF USER DEFINED MAPPER FUNCTIONS #


# TODO: this is pretty bad, need to review how links are stored on a feature
def map_relations(relations_set, f):
    area = f["properties"]["dauid"]
    hospitals = f["properties"]["hospitals"]
    hospitals = [h.strip() for h in hospitals.split(',')]

    for i, hospital in enumerate(hospitals):
        relations_set[i]["links"].append([area, hospital])
        relations_set[3]["links"].append([hospital, area])


# END OF USER DEFINED MAPPER FUNCTIONS #
# read geojson files as json data
d_areas = get_geojson_data('../output/emergency_areas.geojson')
d_hospitals = get_geojson_data('../output/hospitals.geojson')

# build instances for each set of data.
# The 1st parameter identifies a model type from the LoM, it is used to retrieve the source file and class name to map onto the data
# The 2nd parameter is a mapper function that converts a data entry into initialization parameters for an instance of model type specified
# The 3rd parameter is the set of data used to build instances
instances = [build_instances(8, map_emergency_area, d_areas),
             build_instances(9, map_hospital, d_hospitals)]

# build empty relations set, this depends on the user's use case
# The 1st parameter identifies a source model type from the LoM, it is used to retrieve the source model type class name
# The 2nd parameter is the source output port used to build the coupling. It must be belong to model type identified above
# The 3rd parameter identifies a target model type from the LoM, it is used to retrieve the target model type class name
# The 4th parameter is the target input port used to build the coupling. It must be belong to model type identified above
relations = [build_empty_relation_set(8, "emergency_area_defs::out_1", 9, "hospital_defs::processor_in"),
             build_empty_relation_set(8, "emergency_area_defs::out_2", 9, "hospital_defs::processor_in"),
             build_empty_relation_set(8, "emergency_area_defs::out_3", 9, "hospital_defs::processor_in"),
             build_empty_relation_set(9, "hospital_defs::processor_out", 8, "emergency_area_defs::rejected_1")]

# Fill the relations set from data, users provide a mapper function.
relations = fill_relation_set(relations, map_relations, d_areas)

with open('../output/auto_instances.json', 'w') as file:
    json.dump(instances, file)

with open('../output/auto_relations.json', 'w') as file:
    json.dump(relations, file)

