from argparse import ArgumentParser

class Args:
    @property
    def workflow(self):
        return self.args.workflow

    def __init__(self):
        parser = ArgumentParser(description='This script is used execute a spatial analysis workflow to generate instances sets and relations sets from geojson data.')
        parser.add_argument('--workflow', dest='workflow', type=str, help='Path to the workflow configuration file', required=True)

        self.args = parser.parse_args()


