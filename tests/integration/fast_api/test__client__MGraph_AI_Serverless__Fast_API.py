from unittest                                                           import TestCase
from osbot_utils.utils.Files                                            import save_bytes_as_file
from mgraph_ai_serverless.testing.mgraph_ai_serverless__objs_for_tests  import mgraph_ai_serverless__fast_api__client


class test__client__MGraph_AI_Serverless__Fast_API(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = mgraph_ai_serverless__fast_api__client

    def test__static__examples(self):
        assert self.client.get('/static/favicon.ico'              ).status_code == 200
        assert self.client.get('/static/examples/hello-world.html').status_code == 200
        assert self.client.get('/static/examples/markdown.html'   ).status_code == 200

    def test_web_root__render_mermaid(self):
        response = self.client.post('/web_root/render-mermaid', json={'mermaid_code': 'graph TD\n    Z-->B\n    A-->C\n    B-->D\n    C-->D'})
        assert response.status_code == 200
        #screenshot_bytes = response.content
        # from pprint import pprint
        # pprint(screenshot_bytes)
        #assert screenshot_bytes.startswith(b'\x89PNG') is True
        #save_bytes_as_file(screenshot_bytes, '/tmp/hello-world.png')