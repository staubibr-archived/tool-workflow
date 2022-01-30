
class Layer:
    @property
    def name(self):
        return self._json["name"]

    @property
    def file(self):
        return self._json["file"]

    def __init__(self, _json):
        self._json = _json

class InstanceSet:
    @property
    def layer(self):
        return self._json["layer"]

    @property
    def model(self):
        return self._json["model"]

    @property
    def id_field(self):
        return self._json["id_field"]

    @property
    def properties(self):
        return self._json["properties"]

    def __init__(self, _json):
        self._json = _json

class RelationSet:
    @property
    def layer(self):
        return self._json["layer"]

    @property
    def coupling(self):
        return self._json["coupling"]

    @property
    def fields(self):
        return self._json["fields"]

    def __init__(self, _json):
        self._json = _json

class Output:
    @property
    def layers(self):
        return self._json["layers"]

    @property
    def instances(self):
        return self._json["instances"]

    @property
    def relations(self):
        return self._json["relations"]

    def __init__(self, _json):
        self._json = _json

        self._json["layers"] = [Layer(j) for j in self.layers]
        self._json["instances"] = [InstanceSet(j) for j in self.instances]
        self._json["relations"] = [RelationSet(j) for j in self.relations]

    def layer(self, name):
        if name not in self.layers:
            raise Exception('Layer {name} is undefined in config data.'.format(name=name))

        return self.layers[name]

class Input:
    @property
    def layers(self):
        return self._json["layers"]

    @property
    def tables(self):
        return self._json["tables"]

    @property
    def parameters(self):
        return self._json["parameters"]

    def __init__(self, _json):
        self._json = _json

    def data(self, name):
        if name not in self.tables:
            raise Exception('Dataset {name} is undefined in config data.'.format(name=name))

        return self.tables[name]

    def layer(self, name):
        if name not in self.layers:
            raise Exception('Layer {name} is undefined in config layers.'.format(name=name))

        return self.layers[name]

    def param(self, name):
        if name not in self.parameters:
            raise Exception('Parameter {name} is undefined in config parameters.'.format(name=name))

        return self.parameters[name]

class Task:
    @property
    def name(self):
        return self._json["name"]

    @property
    def params(self):
        return self._json["params"]

    @property
    def output(self):
        return self._json["output"]

    @property
    def json(self):
        return self._json

    def __init__(self, _json):
        if "output" not in _json:
            _json["output"] = None

        self._json = _json

class Config:
    @property
    def output(self):
        return self._json["output"]

    @property
    def input(self):
        return self._json["input"]

    @property
    def tasks(self):
        return self._json["tasks"]

    @property
    def output_folder(self):
        return self._output_folder

    @property
    def input_folder(self):
        return self._input_folder

    def __init__(self, json, input_folder, output_folder):
        self._input_folder = input_folder
        self._output_folder = output_folder
        self._json = json

        self._json["tasks"] = [Task(j) for j in self.tasks]
        self._json["output"] = Output(self.output)
        self._json["input"] = Input(self.input)

    def output_path(self, name):
        return self.output_folder + "/" + name

    def input_layer(self, name):
        return self.input_folder + "/" + self.input.layer(name)

    def input_data(self, name):
        return self.input_folder + "/" + self.input.data(name)
