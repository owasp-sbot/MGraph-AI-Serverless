import mgraph_ai_serverless
from unittest                                                           import TestCase
from osbot_utils.utils.Files                                            import file_contents, path_combine
from mgraph_ai_serverless.testing.mgraph_ai_serverless__objs_for_tests  import  mgraph_ai_serverless__fast_api__app
from osbot_fast_api.utils.Fast_API_Server                               import Fast_API_Server

class test__http__MGraph_AI_Serverless__Fast_API(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fast_api_server = Fast_API_Server(app=mgraph_ai_serverless__fast_api__app)
        cls.fast_api_server.start()
        assert cls.fast_api_server.is_port_open() is True

    @classmethod
    def tearDownClass(cls):
        cls.fast_api_server.stop()
        assert cls.fast_api_server.is_port_open() is False

    def test_http__info_version(self):
        response = self.fast_api_server.requests_get('/info/version')
        assert response.status_code == 200

    def test__static__examples(self):
        assert self.fast_api_server.requests_get('/static/favicon.ico'              ).status_code == 200
        assert self.fast_api_server.requests_get('/static/examples/markdown.html'   ).status_code == 200
        response__hello_world = self.fast_api_server.requests_get('/static/examples/hello-world.html')

        path_file__hello_world = path_combine(mgraph_ai_serverless.path, 'web_root/examples/hello-world.html')
        contents__hello_world  = file_contents(path_file__hello_world)
        assert response__hello_world.status_code == 200
        assert response__hello_world.text        == contents__hello_world

    # def test__http__root__render_mermaid(self):
    #     assert self.fast_api_server.requests_post('/web_root/render-mermaid' ).status_code == 200
