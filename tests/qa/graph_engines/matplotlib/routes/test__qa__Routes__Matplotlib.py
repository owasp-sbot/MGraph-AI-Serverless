import pytest
import requests
from dataclasses                                                                        import asdict
from unittest                                                                           import TestCase
from mgraph_ai.providers.json.MGraph__Json                                              import MGraph__Json
from mgraph_ai.providers.simple.MGraph__Simple__Test_Data                               import MGraph__Simple__Test_Data
from mgraph_ai_serverless.graph_engines.matplotlib.models.Model__Matplotlib__Render     import Model__Matplotlib__Render
from osbot_utils.utils.Http                                                             import url_join_safe
from osbot_utils.utils.Env                                                              import get_env, load_dotenv

ENV_VAR_NAME__QA_LAMBDA = 'ENDPOINT_URL__QA_LAMBDA'

class test__qa__Routes__Matplotlib(TestCase):

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

    def test__1__matplotlib__render_simple_graph(self):
        target_url       = self.get_url('/matplotlib/render-graph')
        render_config    = Model__Matplotlib__Render(graph_data       = self.test_graph.graph.json())
        response         = requests.post(target_url, json=asdict(render_config))
        screenshot_bytes = response.content

        assert response.status_code                    == 200
        assert screenshot_bytes.startswith(b'\x89PNG') is True

        #file_create_from_bytes('/tmp/matplotlib_simple.png', screenshot_bytes)

    def test__2__matplotlib__render_json_graph(self):
        target_url = self.get_url('/matplotlib/render-graph')

        test_data = { "string" : "value"           ,
                      "number" : 42                ,
                      "boolean": True              ,
                      "null"   : None              ,
                      "array"  : [1, 2, 3,5]         ,
                      "object" : {"key": "value"   }}

        mgraph_json = MGraph__Json()
        mgraph_json.load().from_data(test_data)

        render_config = Model__Matplotlib__Render(graph_data = mgraph_json.graph.json(),
                                                  layout     = 'circular'              )
        response = requests.post(target_url, json=asdict(render_config))
        screenshot_bytes = response.content

        assert response.status_code                    == 200
        assert screenshot_bytes.startswith(b'\x89PNG') is True

        #file_create_from_bytes('./matplotlib_json.png', screenshot_bytes)

    def test__3__matplotlib__render_formats(self):
        target_url = self.get_url('/matplotlib/render-graph')
        formats = ['png', 'svg', 'pdf']

        for format in formats:
            render_config = Model__Matplotlib__Render(graph_data    = self.test_graph.graph.json(),
                                                      output_format = format                      )

            response = requests.post(target_url, json=asdict(render_config))
            assert response.status_code == 200
            assert response.headers['content-type'] == f'image/{format}'

            #file_create_from_bytes(f'/tmp/matplotlib_format_{format}.{format}', response.content)

    def test__4__matplotlib__render_layouts(self):
        target_url = self.get_url('/matplotlib/render-graph')
        layouts = ['spring', 'circular', 'random', 'shell', 'spectral']

        for layout in layouts:
            render_config = Model__Matplotlib__Render(graph_data= self.test_graph.graph.json(),
                                                      layout    = layout                      )

            response = requests.post(target_url, json=asdict(render_config))
            assert response.status_code == 200
            assert response.headers['content-type'] == 'image/png'

            #file_create_from_bytes(f'/tmp/matplotlib_layout_{layout}.png',response.content)