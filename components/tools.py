import os
import json

from qgis.core import QgsVectorFileWriter, QgsCoordinateReferenceSystem

def empty_folder(dir):
    for path in os.listdir(dir):
        full_path = os.path.join(dir, path)

        if os.path.isfile(full_path):
            os.remove(full_path)

def save_layer(layer, path_output):
    crs = QgsCoordinateReferenceSystem("epsg:4326")

    QgsVectorFileWriter.writeAsVectorFormat(layer, path_output, 'utf-8', crs, 'GeoJSON', layerOptions=['RFC7946=True'])

def get_geojson_data(path):
    d = json.load(open(path))

    return d["features"]









