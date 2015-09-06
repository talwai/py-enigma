from __future__ import print_function

from functools import partial
import requests
import json

class Endpoints(object):
    DATA = 'data'
    METADATA = 'meta'
    STATS = 'stats'
    EXPORT = 'export'

class Sort(object):
    ASCENDING = '+'
    DESCENDING = '-'

class Operations(object):
    SUM = "sum"
    AVG = "avg"
    STD_DEV = "stddev"
    VARIANCE = "variance"
    MAX = "max"
    MIN = "min"
    FREQUENCY = "frequency"

class UnsupportedMethod(Exception): pass

class Client(object):
    VERSION = 'v2'

    class Metadata(object): pass
    class Stats(object): pass
    class Data(object): pass
    class ExportRequest(object): pass

    def __init__(self, api_key):
        self.api_key = api_key
        self._current_query = None

        setattr(self.Metadata, 'query', self._metadata_query)
        setattr(self.Stats, 'query', self._stats_query)
        setattr(self.Data, 'query', self._data_query)
        setattr(self.ExportRequest, 'new', self._export_request)

    def format_request(self, version, endpoint, datapath, params):
        return 'https://api.enigma.io/{0}/{1}/{2}/{3}/{4}'\
                .format(version, endpoint, self.api_key, datapath, params)

    def query(self, endpoint, datapath, params):
        try:
            params = json.dumps(params)
            req = self.format_request(
                    self.VERSION,
                    endpoint,
                    datapath,
                    params)
            resp = requests.get(req)
            self._current_query = req
        except requests.exceptions.Timeout:
            print("Request timed out!")
            raise

        resp.raise_for_status()
        return resp.json()

    def _query_head(self, endpoint):
            resp = requests.get(endpoint)
            #self._current_query = req
            return resp

    def _metadata_query(self, datapath, params):
        return EnigmaResource.from_json(
                self.query(Endpoints.METADATA, datapath, params),
                self._current_query
        )

    def _data_query(self, datapath, params):
        return EnigmaResource.from_json(
                self.query(Endpoints.DATA, datapath, params),
                self._current_query
        )

    def _stats_query(self, datapath, params):
        return EnigmaResource.from_json(
                self.query(Endpoints.STATS, datapath, params),
                self._current_query
        )

    def _export_request(self, datapath, params):
        resp = self.query(Endpoints.EXPORT, datapath, params)
        head_url = resp['head_url']
        export_url = resp['export_url']

        resp = self._query_head(head_url)

class EnigmaResource(object):
    def __init__(self, info, datapath, result, query):
        self.info = info
        self.datapath = datapath
        self.result = result
        self._query = query # The query that produced this resource

    @classmethod
    def from_json(cls, json_dct, query):
        info = json_dct.get('info')
        datapath = json_dct.get('datapath')
        result = json_dct.get('result')
        return cls(info, datapath, result, query)

class EnigmaQuery(object):
    def __init__(self, version, endpoint, api_key, datapath, params):
        self.version = version
        self.endpoint = endpoint
        self.api_key = api_key
        self.datapath = datapath
        self.params = params

    @classmethod
    def from_string(cls, query_string):
        assert query_string.find('https://api.enigma.io/') != -1
        _, parts = query_string.split('https://api.enigma.io/')[0], query_string.split('https://api.enigma.io/')[1].split('/')
        return cls(parts[0], parts[1], parts[2], parts[3], parts[4])

    def __eq__(self, other):
        return self.version == other.version\
            and self.endpoint == other.endpoint\
            and self.api_key == other.api_key\
            and self.datapath == other.datapath\
            and json.loads(self.params) == json.loads(other.params)
