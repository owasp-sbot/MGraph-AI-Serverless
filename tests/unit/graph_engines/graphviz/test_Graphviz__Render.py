from unittest                                                       import TestCase
from mgraph_ai.providers.json.MGraph__Json                          import MGraph__Json
from osbot_utils.utils.Files                                        import file_exists, file_delete
from mgraph_ai.providers.simple.MGraph__Simple__Test_Data           import MGraph__Simple__Test_Data
from mgraph_ai_serverless.graph_engines.graphviz.Graphviz__Render   import Graphviz__Render


class test_Graphviz__Render(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.graphviz_render = Graphviz__Render()
        cls.test_graph      = MGraph__Simple__Test_Data().create()
        cls.dot_text        = cls.test_graph.export().to__dot()

    def test_render_dot(self):
        with self.graphviz_render as _:
            created_file = _.render_dot(self.dot_text)
            assert file_exists(created_file) is True
            assert file_delete(created_file) is True

    def test_render_dot__json_mgraph(self):
        mgraph    = MGraph__Json()
        test_data = { "string" : "value"         ,
                      "number" : 42              ,
                      "boolean": True            ,
                      "null"   : None            ,
                      "array"  : [1, 2, 3]       ,
                      "object" : {"key": "value"}}

        mgraph.load().from_json(test_data)
        dot_text = mgraph.export().to_dot().to_string()
        with self.graphviz_render as _:
            created_file = _.render_dot(dot_text)
            assert file_exists(created_file) is True
            assert file_delete(created_file) is True



