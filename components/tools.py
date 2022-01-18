import os
import json

from qgis.core import QgsVectorFileWriter, QgsCoordinateReferenceSystem, QgsCoordinateTransformContext, QgsCoordinateTransform

def empty_folder(dir):
    for path in os.listdir(dir):
        full_path = os.path.join(dir, path)

        if os.path.isfile(full_path):
            os.remove(full_path)

def save_layer(layer, path_output):
    source_crs = layer.sourceCrs()
    target_crs = QgsCoordinateReferenceSystem("epsg:4326")
    context = QgsCoordinateTransformContext()

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GeoJSON"
    options.ct = QgsCoordinateTransform(source_crs, target_crs, context)

    # QgsVectorFileWriter.writeAsVectorFormat(layer, path_output, 'utf-8', crs, 'GeoJSON', layerOptions=['RFC7946=True'])

    QgsVectorFileWriter.writeAsVectorFormatV2(layer, path_output, QgsCoordinateTransformContext(), options)


def get_json(path):
    with open(path, 'r') as content:
        return json.load(content)

def get_geojson_data(path):
    d = get_json

    return d["features"]









