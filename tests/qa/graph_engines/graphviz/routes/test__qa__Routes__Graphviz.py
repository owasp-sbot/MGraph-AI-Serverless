import pytest
import requests
from unittest                                             import TestCase
from mgraph_ai.providers.json.MGraph__Json                import MGraph__Json
from mgraph_ai.providers.simple.MGraph__Simple__Test_Data import MGraph__Simple__Test_Data
from osbot_utils.utils.Http                               import url_join_safe
from osbot_utils.utils.Env                                import get_env, load_dotenv

ENV_VAR_NAME__QA_LAMBDA = 'ENDPOINT_URL__QA_LAMBDA'
ROUTE__RENDER__PATH     = '/graphviz/render-dot'
FILE__GRAPH_SCREENSHOT  = './graphviz-dot.png'

class test__qa__Routes__Graphviz(TestCase):

    @classmethod
    def setUp(cls):
        load_dotenv()
        cls.target_server = get_env(ENV_VAR_NAME__QA_LAMBDA)
        #cls.target_server = "http://0.0.0.0:8080/"
        if not cls.target_server:
            pytest.skip(f"{ENV_VAR_NAME__QA_LAMBDA} env var not set")
        cls.test_graph = MGraph__Simple__Test_Data().create()

    def get_url(self, path):
        return url_join_safe(self.target_server, path)

    def create_json_payload(self, dot_source):
        payload = {"dot_source"   : dot_source,
                   "output_format": "png"     }
        return payload

    def create_screenshot(self, dot_source):
        target_url       = self.get_url(ROUTE__RENDER__PATH)
        payload          = self.create_json_payload(dot_source)
        response         = requests.post(target_url, json=payload)
        screenshot_bytes = response.content
        assert response.status_code                    == 200
        assert screenshot_bytes.startswith(b'\x89PNG') is True
        return screenshot_bytes

    def save_screenshot(self, screenshot_bytes):
        from osbot_utils.utils.Files import file_create_from_bytes
        file_create_from_bytes(FILE__GRAPH_SCREENSHOT, screenshot_bytes)

    def test__1__graphviz__render_simple_graph(self):
        dot_source       = self.test_graph.export().to__dot()
        screenshot_bytes = self.create_screenshot(dot_source)
        assert 12_000 < len(screenshot_bytes) < 15_000
        #self.save_screenshot(screenshot_bytes)


    def test__2__graphviz__render_json_graph(self):
        test_data  = { "string" : "value"           ,
                       "number" : 42                ,
                       "boolean": True              ,
                       "null"   : None              ,
                       "array"  : [1, 2, 3,4,5,6,7,8,9,10, {'a':'b', 'c':'d', 'e':[1,2,3,4]}]         ,
                       "object" : {"key": "value"   }}

        mgraph_json = MGraph__Json()
        mgraph_json.load().from_data(test_data)
        dot_source       = mgraph_json.export().to_dot().to_string()
        screenshot_bytes = self.create_screenshot(dot_source)
        assert 150_000 < len(screenshot_bytes) < 200_000
        #self.save_screenshot(screenshot_bytes)