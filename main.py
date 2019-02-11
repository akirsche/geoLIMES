#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from sys import path

from config import load_config
from geolimes import goeLIMES

path.append("${HOME}/.local/lib/python3.7/site-packages/")


def get_arguments():
    parser = ArgumentParser(description="Python LIMES")
    parser.add_argument("-c", "--config", type=str, dest="config_file", help="Path to a config file", required=True)
    parser.add_argument("-d", "--database", type=str, dest="database_config_file", help="Path to a database config file", required=True)
    parser.add_argument("-v", "--version", action="version", version="0.0.1", help="Show program version and exit")
    arguments = parser.parse_args()
    return arguments.config_file, arguments.database_config_file


<<<<<<< HEAD
def create_dirs():
    if not exists('logs') or not isdir('logs'):
        makedirs('logs')

    if not exists('output') or not isdir('output'):
        makedirs('output')


def run(config_string, database_config_string, to_file=True):
    # TODO: Quick fix for Hackatron -> Needs better handling when using api
    if database_config_string == None:
        database_config_string = load_config('../geoLIMES/configs/postgresql.json')

    create_dirs()
    results = None

    try:
        config_json = loads(config_string)
        database_config = loads(database_config_string)
        config = Config(config_json, database_config)

        source_sparql = SPARQL(config, 'source')
        target_sparql = SPARQL(config, 'target')

        info_logger = InfoLogger('InfoLogger', '{}_{}'.format(source_sparql.get_query_hash(), target_sparql.get_query_hash()))

        source_cache = Cache(info_logger,  config, source_sparql, 'source')
        source_cache.create_cache()

        target_cache = Cache(info_logger, config, target_sparql, 'target')
        target_cache.create_cache()

        mapper = Mapper(info_logger, config, source_sparql, target_sparql)
        results = mapper.map(to_file)
    except ConfigNotValidError as e:
        results = "Config not valid"
        print(e)
    except HTTPError as e:
        print(e)
    except JSONDecodeError as e:
        print(e)

    return results


=======
>>>>>>> fbe283fba1b18701e9ed5289acf94f9515579177
def main():
    try:
        connfig_file_path, database_config_file_path = get_arguments()
        config = load_config(connfig_file_path)
        database_config = load_config(database_config_file_path)
        limes = goeLIMES(database_config)
        limes.run(config)
    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()
