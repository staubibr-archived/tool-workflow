import json


class Target:
    @property
    def model_type_id(self):
        return self._model_type_id

    @property
    def port(self):
        return self._port

    def __init__(self, model_type_id, port):
        self._model_type_id = model_type_id
        self._port = port

    def same(self, model_type_id, port):
        return self.model_type_id == model_type_id and self.port == port

    def to_json(self):
        return {
            "model_type_id": self.model_type_id,
            "port": self.port
        }

class RelationsSet:
    @property
    def source(self):
        return self._source

    @property
    def destination(self):
        return self._destination

    @property
    def links(self):
        return self._links

    def __init__(self, source=None, destination=None, links=None):
        self._source = source
        self._destination = destination
        self._links = [] if links is None else links

    # areas, dauid, hospitals
    def fill(self, layer, f_src, f_dest):
        for f in layer.getFeatures():
            self.links.append([f[f_src], f[f_dest]])

    def same(self, src_model_type_id, src_port, tgt_model_type_id, tgt_port):
        return self.source.same(src_model_type_id, src_port) and self.destination.same(tgt_model_type_id, tgt_port)

    def to_cbm(self):
        return {
            "from_model": self.source.model_type_id,
            "from_port": self.source.port,
            "to_model": self.destination.model_type_id,
            "to_port": self.destination.port,
            "links": self.links
        }

    def to_json(self):
        return {
            "source": self.source.to_json(),
            "destination": self.destination.to_json(),
            "links": self.links
        }

class RelationsSets:
    @property
    def sets(self):
        return self._sets

    def __init__(self):
        self._sets = list()

    def get_set(self, source_model_type, source_port, destination_model_type, destination_port):
        for s in self.sets:
            if s.same(source_model_type, source_port, destination_model_type, destination_port):
                return s

        return None

    def add_set(self, source_model_type, source_port, destination_model_type, destination_port):
        s = self.get_set(source_model_type, source_port, destination_model_type, destination_port)

        if s is not None:
            return s

        s = RelationsSet(Target(source_model_type, source_port), Target(destination_model_type, destination_port))

        self._sets.append(s)

        return s

    def fill(self, mapper, layer):
        for f in layer.getFeatures():
            mapper(self, f)

    def to_json(self):
        return [relations_set.to_json() for relations_set in self._sets]

    def to_cbm(self):
        return [relations_set.to_cbm() for relations_set in self._sets]

    def dump(self, path):
        with open(path, 'w') as file:
            json.dump(self.to_json(), file)