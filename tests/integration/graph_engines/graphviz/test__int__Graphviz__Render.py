from unittest                                                                       import TestCase
from mgraph_ai.providers.json.MGraph__Json                                          import MGraph__Json
from mgraph_ai.providers.simple.MGraph__Simple__Test_Data                           import MGraph__Simple__Test_Data
from mgraph_ai_serverless.graph_engines.graphviz.Graphviz__Render                   import Graphviz__Render
from mgraph_ai_serverless.graph_engines.graphviz.models.Model__Graphviz__Render_Dot import Model__Graphviz__Render_Dot


class test__int__Graphviz__Render(TestCase):

    @classmethod
    def setUpClass(cls):                                                        # Setup test data
        cls.graphviz_render = Graphviz__Render()
        cls.test_graph      = MGraph__Simple__Test_Data().create()
        cls.dot_text        = cls.test_graph.export().to__dot()

    def test_render_dot(self):                                                  # Test PNG rendering
        with self.graphviz_render as _:
            render_config = Model__Graphviz__Render_Dot(dot_source=self.dot_text)
            result = _.render_dot(render_config)
            assert isinstance(result, bytes)
            assert len(result) > 0

    def test_render_dot__json(self):                                     # Test with JSON data
        mgraph    = MGraph__Json()
        test_data = { "string" : "value"         ,
                      "number" : 42              ,
                      "boolean": True            ,
                      "null"   : None            ,
                      "array"  : [1, 2, 3]       ,
                      "object" : {"key": "value"}}

        mgraph.load().from_data(test_data)
        dot_text = mgraph.export().to_dot().to_string()

        with self.graphviz_render as _:
            render_config = Model__Graphviz__Render_Dot(dot_source=dot_text)
            result = _.render_dot(render_config)
            assert isinstance(result, bytes)
            assert len(result) > 0