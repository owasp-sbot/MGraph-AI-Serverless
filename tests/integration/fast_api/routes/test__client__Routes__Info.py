from unittest                                                           import TestCase
from mgraph_ai_serverless.testing.mgraph_ai_serverless__objs_for_tests import mgraph_ai_serverless__fast_api__client
from mgraph_ai_serverless.utils.Version                           import version__mgraph_ai_serverless



class test__client__Routes__Info(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = mgraph_ai_serverless__fast_api__client

    def test_raw__uk__homepage(self):
        response = self.client.get('/info/version')
        assert response.status_code == 200
        assert response.json()      == {'version': version__mgraph_ai_serverless }

