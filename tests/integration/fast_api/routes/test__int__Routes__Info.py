from unittest                                           import TestCase
from mgraph_ai_serverless.fast_api.routes.Routes__Info  import Routes__Info
from mgraph_ai_serverless.utils.Version                 import version__mgraph_ai_serverless


class test__int__Routes__Info(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.routes_mgraph_ai_serverless = Routes__Info()

    def test_routes_setup(self):
        with self.routes_mgraph_ai_serverless as _:
            assert _.tag == 'info'
            _.setup_routes()
            assert '/version' in _.routes_paths()

    def test__version(self):
        with self.routes_mgraph_ai_serverless as _:
            assert _.version() == { 'version': version__mgraph_ai_serverless }
