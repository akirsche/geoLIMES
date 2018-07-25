#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from csv import reader, writer
from fiona import collection
from os.path import join, isfile
from rtree import Rtree
from rtree.index import Index
from shapely.geometry import mapping, shape
from shapely.wkt import loads

from logger import InfoLogger

import logging
import pickle
import time


class Cache:
    def __init__(self, config, sparql, type):
        self.config = config
        self.sparql = sparql
        self.type = type

        self.info_logger = InfoLogger('InfoLogger', sparql.get_query_hash())

    def create_cache_chunks(self, index=False):
        if isfile(join('cache', '{}.csv'.format(self.sparql.query_hash))):
            self.info_logger.logger.log(logging.INFO, "Cache file {}.csv for query already exists".format(self.sparql.query_hash))
            self.info_logger.logger.log(logging.INFO, "Loading cache file...")
            with open('cache/{}.csv'.format(self.sparql.query_hash), 'r') as cache_file:
                items = list(reader(cache_file, delimiter=';'))

                if index:
                    if not isfile(join('cache', '{}.idx'.format(self.sparql.query_hash))):
                        self.write_index_file(items)

                return items

        offset = self.config.get_offset(self.type)
        limit = self.config.get_limit(self.type)
        chunksize = self.config.get_chunksize(self.type)
        results = []
        run = True

        start = time.time()

        while(run):
            if limit > 0 and offset + chunksize >= limit:
                chunksize = limit - offset
                run = False

            self.info_logger.logger.log(logging.INFO, "Getting statements from {} to {}".format(offset, offset + chunksize))
            result = self.sparql.query(offset, chunksize)
            result_info = result.info()

            if 'x-sparql-maxrows' in result_info:
                max_chunksize_server = int(result_info['x-sparql-maxrows'])

                if max_chunksize_server and max_chunksize_server < chunksize:
                    chunksize = max_chunksize_server
                    self.info_logger.logger.log(
                        logging.INFO, "Max server rows is smaller than chunksize, new chunksize is {}".format(max_chunksize_server))

            offset = offset + chunksize

            uri_idx = -1
            shape_idx = -1

            for idx, item in enumerate(result):
                item_decoded = item.decode('utf-8')
                item_split = item_decoded.split('","')

                if idx == 0:
                    for split_index, split in enumerate(item_split):
                        split = split.replace('"', '').replace('\n', '')

                        if split == self.config.get_var_uri(self.type):
                            uri_idx = split_index

                        if split == self.config.get_var_shape(self.type):
                            shape_idx = split_index
                elif idx > 0:
                    items = [None, None]

                    for split_index, split in enumerate(item_split):
                        split = split.replace('"', '').replace('\n', '')

                        if split_index == uri_idx:
                            items[0] = split
                        elif split_index == shape_idx:
                            items[1] = split

                    if items[0] and items[1]:
                        results.append(items)

        end = time.time()
        self.info_logger.logger.log(logging.INFO, "Retrieving statements took {}".format(round(end - start, 4)))

        self.write_cache_file(results)

        if index:
            self.write_index_file(results)

        return results

    def write_cache_file(self, results):
        self.info_logger.logger.log(logging.INFO, "Writing cache file: {}.csv".format(self.sparql.query_hash))

        with open(join('cache', '{}.csv'.format(self.sparql.query_hash)), 'w') as cache_file:
            csvWriter = writer(cache_file, delimiter=';')
            csvWriter.writerows(results)

    def write_index_file(self, results):
        self.info_logger.logger.log(logging.INFO, "Writing index file for {}".format(self.sparql.query_hash))

        idx = FastRetree(join('cache', self.sparql.query_hash), rtree_generator(results))
        idx.close()


class FastRetree(Rtree):
    def dumps(self, obj):
        return pickle.dumps(obj, -1)


def rtree_generator(items):
    for i, item in enumerate(items):
        uri = item[0]
        geometry = loads(item[1])

        if not geometry.is_empty:  # Exclude empty geometry
            yield (i, geometry.bounds, None)
