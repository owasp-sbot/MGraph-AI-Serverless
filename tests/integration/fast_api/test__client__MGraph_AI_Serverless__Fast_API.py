from unittest                                                           import TestCase
from mgraph_ai_serverless.testing.mgraph_ai_serverless__objs_for_tests  import mgraph_ai_serverless__fast_api__client


class test__client__MGraph_AI_Serverless__Fast_API(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = mgraph_ai_serverless__fast_api__client

    def test__static__examples(self):
        assert self.client.get('/static/favicon.ico'              ).status_code == 200
        assert self.client.get('/static/examples/hello-world.html').status_code == 200
        assert self.client.get('/static/examples/markdown.html'   ).status_code == 200

