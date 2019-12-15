import os

import yaml

directory = os.path.split(os.path.abspath(__file__))[0]

with open(os.path.join(directory, 'variables.yml'), 'r') as stream:
    variables = yaml.safe_load(stream)
