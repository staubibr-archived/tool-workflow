
from PyQt5.QtCore import QVariant

def execute(src_layer, src_id_field, updates):
    for feature in src_layer.getFeatures():
        src_id = feature[src_id_field]

        if src_id not in updates:
            continue

        src_layer.startEditing()

        for f, v in updates[src_id].items():
            i_field = src_layer.fields().indexFromName(f)
            field = src_layer.dataProvider().fields()[i_field]

            if field.type() == QVariant.Int:
                test =  src_layer.changeAttributeValue(feature.id(), i_field, int(v))
                x = 1

            elif field.type() == QVariant.Double:
                test =  src_layer.changeAttributeValue(feature.id(), i_field, float(v))
                x = 1

            else:
                test = src_layer.changeAttributeValue(feature.id(), i_field, v)
                x = 1

    src_layer.commitChanges()

    return src_layer

def auto_execute(params):
    layer = params["INPUT"]
    id_field = params["ID_FIELD"]
    updates = params["UPDATES"]

    return execute(layer, id_field, updates)
