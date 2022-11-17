import yaml
from yaml.loader import SafeLoader


def read_yaml_file(file_name):
    """ Read an yml file and return its data"""
    with open(file_name, 'r') as stream:
        return yaml.load(stream, Loader=SafeLoader)


def request_yaml_config_file():
    """ Request the config file and returns the user input"""
    return input("Config File: ")
