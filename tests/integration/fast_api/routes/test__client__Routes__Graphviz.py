from unittest                                                                       import TestCase
from osbot_utils.utils.Files                                                        import file_create_from_bytes
from mgraph_ai_serverless.graph_engines.graphviz.models.Model__Graphviz__Render_Dot import GRAPHVIZ__DOT__SAMPLE_GRAPH_1
from mgraph_ai_serverless.testing.mgraph_ai_serverless__objs_for_tests              import mgraph_ai_serverless__fast_api__client

class test__client__Routes__Graphviz(TestCase):

    @classmethod
    def setUpClass(cls):                                                        # Setup test client
        cls.client = mgraph_ai_serverless__fast_api__client

    def test_render_dot(self):                                                  # Test client POST
        payload = { "dot_source"   : GRAPHVIZ__DOT__SAMPLE_GRAPH_1 ,
                    "output_format": "png"                       }
        response = self.client.post('/graphviz/render-dot', json=payload)
        assert response.status_code == 200
        assert len(response.content) > 0
        assert type(response.content) is bytes
        file_create_from_bytes('/tmp/graphviz_render_dot.png', response.content)
