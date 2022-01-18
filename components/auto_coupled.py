import json

class AutoCoupled:
    @property
    def id(self):
        return self._id

    @property
    def model_type_id(self):
        return self._model_type_id

    @property
    def instances_sets(self):
        return self._instances_sets

    @property
    def relations_sets(self):
        return self._relations_sets

    def __init__(self, id, model_type_id, instances_sets, relations_sets):
        self._id = id
        self._model_type_id = model_type_id
        self._instances_sets = instances_sets
        self._relations_sets = relations_sets

    def to_json(self):
        return {
            "id": self.id,
            "model_type_id": self.model_type_id,
            "instances": self.instances_sets.to_json(),
            "relations": self.relations_sets.to_json()
        }

    def to_cbm(self):
        return {
            "id": self.id,
            "model_type": self.model_type_id,
            "components": self.instances_sets.to_cbm(),
            "couplings": self.relations_sets.to_cbm()
        }

    def dump(self, path):
        with open(path, 'w') as file:
            json.dump(self.to_json(), file)

    def dump_cbm(self, path):
        with open(path, 'w') as file:
            json.dump(self.to_cbm(), file)
