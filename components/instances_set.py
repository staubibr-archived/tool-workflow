import json


class Instance:
    @property
    def id(self):
        return self._id

    @property
    def params(self):
        return self._params

    def __init__(self, id, params):
        self._id = id
        self._params = params

    def to_json(self):
        return {
            "id": self.id,
            "params": self.params
        }

class InstancesSet:
    @property
    def model_type_id(self):
        return self._model_type_id

    @property
    def instances(self):
        return self._instances

    def __init__(self, model_type_id, instances):
        self._model_type_id = model_type_id
        self._instances = instances

    @staticmethod
    def map_instance(f, id_field, param_fields):
        params = {}

        for p_field in param_fields:
            params[p_field] = f[p_field]

        return Instance(f[id_field], params)

    @staticmethod
    def from_layer(model_type_id, layer, id_field, param_fields):
        def mapper(f):
            return InstancesSet.map_instance(f, id_field, param_fields)

        return InstancesSet(model_type_id, list(map(mapper, layer.getFeatures())))

    def to_json(self):
        return {
            "model_type_id": self.model_type_id,
            "instances": [instance.to_json() for instance in self.instances]
        }

class InstancesSets:
    @property
    def sets(self):
        return self._sets

    def __init__(self):
        self._sets = list()

    def add_set(self, instances_set):
        self._sets.append(instances_set)

    def add_set_from_layer(self, model_type_id, layer, id_field, param_fields):
        self.add_set(InstancesSet.from_layer(model_type_id, layer, id_field, param_fields))

    def to_json(self):
        return [instances_set.to_json() for instances_set in self._sets]

    def dump(self, path):
        with open(path, 'w') as file:
            json.dump(self.to_json(), file)
