import os
import unittest

from enigma import client

TEST_API_KEY = os.environ.get('ENIGMA_TEST_API_KEY', '4dcb5be644ffb08820b71d8c8abe4490')

class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = client.Client(TEST_API_KEY)

    def _assert_query_equals(self, result, query_string):
        res_query = client.EnigmaQuery.from_string(result)
        to_match = client.EnigmaQuery.from_string(query_string)
        assert res_query == to_match

    def test_data_query(self):
        result = self.client.Data.query("us.gov.whitehouse.visitor-list", {'search':'john'})
        self.assertTrue(isinstance(result, client.EnigmaResource))
        self.assertTrue(isinstance(result.result, list))
        self.assertGreater(len(result.result), 0)
        self._assert_query_equals(result._query, 'https://api.enigma.io/v2/data/{0}/us.gov.whitehouse.visitor-list/{{"search": "john"}}'.format(TEST_API_KEY))

    def test_metadata_query(self):
        result = self.client.Metadata.query("us.gov.whitehouse.visitor-list", {'search':'john'})
        self.assertTrue(isinstance(result, client.EnigmaResource))
        self.assertTrue(isinstance(result.result, dict))
        self._assert_query_equals(result._query, 'https://api.enigma.io/v2/meta/{0}/us.gov.whitehouse.visitor-list/{{"search": "john"}}'.format(TEST_API_KEY))

    def test_stats_query(self):
        result = self.client.Stats.query("us.gov.whitehouse.visitor-list", {'select':'total_people','search':'john'})
        self.assertTrue(isinstance(result, client.EnigmaResource))
        self.assertTrue(isinstance(result.result, dict))

        expected = 'https://api.enigma.io/v2/stats/{0}/us.gov.whitehouse.visitor-list/{{"search": "john", "select":"total_people"}}'.format(TEST_API_KEY)
        self._assert_query_equals(result._query, expected)

    def test_export_query(self):
        result = self.client.ExportRequest.new("us.gov.whitehouse.visitor-list", {'select':'total_people','search':'john'})


if __name__ == '__main__':
    unittest.main()
