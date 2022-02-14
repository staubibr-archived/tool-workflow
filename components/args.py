from argparse import ArgumentParser

class Args:
    @property
    def workflow(self):
        return self.args.workflow

    @property
    def output(self):
        return self.args.output

    @property
    def input(self):
        return self.args.input

    @property
    def params(self):
        return self.args.params

    def __init__(self):
        parser = ArgumentParser(description='This script is used execute a spatial analysis workflow to generate instances sets and relations sets from geojson data.')
        parser.add_argument('--workflow', dest='workflow', type=str, help='Path to the workflow configuration file', required=True)
        parser.add_argument('--output', dest='output', type=str, help='Path to the output folder', required=True)
        parser.add_argument('--input', dest='input', type=str, help='Path to the input folder', required=True)
        parser.add_argument('--params', dest='params', type=str, help='Path to the parameter file', required=False)

        self.args = parser.parse_args()


