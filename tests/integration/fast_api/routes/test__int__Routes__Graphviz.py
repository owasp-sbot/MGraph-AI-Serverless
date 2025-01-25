from unittest                                                                       import TestCase
from starlette.testclient                                                           import TestClient
from mgraph_ai_serverless.graph_engines.graphviz.models.Model__Graphviz__Render_Dot import GRAPHVIZ__DOT__SAMPLE_GRAPH_1
from mgraph_ai_serverless.lambdas.handler                                           import app


class test__int__Routes__Graphviz(TestCase):

    @classmethod
    def setUpClass(cls):                                                        # Setup test client
        cls.client = TestClient(app)

    def test_render_dot(self):                                                  # Test POST endpoint
        payload = { "dot_source"   : GRAPHVIZ__DOT__SAMPLE_GRAPH_1 ,
                    "output_format": "png"                          }
        response = self.client.post("/graphviz/render-dot", json=payload)
        assert response.status_code == 200
        assert len(response.content) > 0
        assert type(response.content) is bytes

    def test_render_dot__empty_payload(self):                                   # Test empty payload
        response = self.client.post("/graphviz/render-dot", json={})
        assert response.status_code == 200                                      # returns valid response