from unittest                                          import TestCase
from mgraph_ai_serverless.fast_api.routes.Routes__Info import Routes__Info
from mgraph_ai_serverless.utils.Version                import version__mgraph_ai_serverless


class test_Routes__Info(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.routes_info = Routes__Info()

    def test_version(self):
        assert self.routes_info.version() == {'version': version__mgraph_ai_serverless}

    def test_setup_routes(self):
        with self.routes_info as _:
            assert _.routes_paths() == []
            _.setup_routes()
            assert _.routes_paths() == ['/ping', '/version' ]