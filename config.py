#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Config:
    def __init__(self, config):
        self.config = config
        self.check_config()

    def check_config(self):
        if 'source' not in self.config:
            raise ConfigNotValidError("Config is missing source")

        if 'target' not in self.config:
            raise ConfigNotValidError("Config is missing target")

        if 'endpoint' not in self.config['source']:
            raise ConfigNotValidError("Config is missing source endpoint")

        if 'var' not in self.config['source']:
            raise ConfigNotValidError("Config is missing source var")
        else:
            if 'uri' not in self.config['source']['var']:
                raise ConfigNotValidError("Variable for uri not specified in  source")

            if 'shape' not in self.config['source']['var']:
                raise ConfigNotValidError("Variable for shape not specified in  source")

        if 'rawquery' not in self.config['source']:
            if 'graph' not in self.config['source']:
                raise ConfigNotValidError("Config is missing source graph")

            if 'property' not in self.config['source']:
                raise ConfigNotValidError("Config is missing source property")

        if 'endpoint' not in self.config['target']:
            raise ConfigNotValidError("Config is missing target endpoint")

        if 'var' not in self.config['target']:
            raise ConfigNotValidError("Config is missing target var")
        else:
            if 'uri' not in self.config['target']['var']:
                raise ConfigNotValidError("Variable for uri not specified in  target")

            if 'shape' not in self.config['target']['var']:
                raise ConfigNotValidError("Variable for shape not specified in  target")

        if 'rawquery' not in self.config['target']:
            if 'graph' not in self.config['target']:
                raise ConfigNotValidError("Config is missing target graph")

            if 'property' not in self.config['target']:
                raise ConfigNotValidError("Config is missing target property")

        if 'measures' not in self.config:
            raise ConfigNotValidError("No measures specified")

    def get_chunksize(self, type):
        if type != 'source' and type != 'target':
            raise Exception("Wrong type (not source or target) specified")

        if 'chunksize' in self.config[type]:
            return self.config[type]['chunksize']
        else:
            return -1

    def get_endpoint(self, type):
        if type != 'source' and type != 'target':
            raise Exception("Wrong type (not source or target) specified")

        return self.config[type]['endpoint']

    def get_geometry(self, type):
        if type != 'source' and type != 'target':
            raise Exception("Wrong type (not source or target) specified")

        return self.config[type]['geometry']

    def get_graph(self, type):
        if type != 'source' and type != 'target':
            raise Exception("Wrong type (not source or target) specified")

        return self.config[type]['graph']

    def get_limit(self, type):
        if type != 'source' and type != 'target':
            raise Exception("Wrong type (not source or target) specified")

        if 'limit' in self.config[type]:
            return self.config[type]['limit']
        else:
            return -1

    def get_measures(self):
        return self.config['measures']

    def get_offset(self, type):
        if type != 'source' and type != 'target':
            raise Exception("Wrong type (not source or target) specified")

        if 'offset' in self.config[type]:
            return self.config[type]['offset']
        else:
            return 0

    def get_prefixes(self):
        if 'prefixes' in self.config:
            return self.config['prefixes']
        else:
            return None

    def get_property(self, type):
        if type != 'source' and type != 'target':
            raise Exception("Wrong type (not source or target) specified")

        return self.config[type]['property']

    def get_rawquery(self, type):
        if type != 'source' and type != 'target':
            raise Exception("Wrong type (not source or target) specified")

        if 'rawquery' in self.config[type]:
            return self.config[type]['rawquery']
        else:
            return None

    def get_restriction(self, type):
        if type != 'source' and type != 'target':
            raise Exception("Wrong type (not source or target) specified")

        if 'restriction' in self.config[type]:
            return self.config[type]['restriction']
        else:
            return None

    def get_var_uri(self, type):
        if type != 'source' and type != 'target':
            raise Exception("Wrong type (not source or target) specified")

        return self.config[type]['var']['uri']

    def get_var_shape(self, type):
        if type != 'source' and type != 'target':
            raise Exception("Wrong type (not source or target) specified")

        return self.config[type]['var']['shape']


class ConfigNotValidError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return(self.error)


def load_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        return config_file.read()
