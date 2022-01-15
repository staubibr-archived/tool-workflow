
from PyQt5.QtCore import QVariant
from qgis.core import QgsField

def __group__(od):
    groups = {}

    for feature in od.getFeatures():
        origin = feature["origin_id"]

        if origin not in groups:
            groups[origin] = []

        groups[origin].append(feature)

    return groups

def execute(od, src_layer, src_id_field, lnk_id_field, n):
    groups = __group__(od)

    src_layer.dataProvider().addAttributes([QgsField(lnk_id_field, QVariant.String, "string")])
    src_layer.updateFields()
    src_layer.startEditing()

    i_lnk_field = src_layer.fields().indexFromName(lnk_id_field)

    for feature in src_layer.getFeatures():
        src_id = feature[src_id_field]

        if src_id not in groups:
            raise Exception("All source features should have an array of OD")

        groups[src_id].sort(key=lambda f: f['total_cost'])

        list_hospitals = list(map(lambda f: f['destination_id'], groups[src_id][0:3]))
        str_hospitals = ", ".join(list_hospitals)

        src_layer.changeAttributeValue(feature.id(), i_lnk_field, str_hospitals)

    src_layer.commitChanges()

    return src_layer

def auto_execute(params):
    layer = params["INPUT"]
    od = params["OD"]
    src_field = params["SOURCE_FIELD"]
    lnk_field = params["LINK_FIELD"]
    n = params["N"]

    return execute(od, layer, src_field, lnk_field, n)
