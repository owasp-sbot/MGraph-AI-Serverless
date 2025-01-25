from unittest import TestCase

from osbot_utils.utils.Files import file_exists

from mgraph_ai.providers.simple.MGraph__Simple__Test_Data import MGraph__Simple__Test_Data
from osbot_utils.utils.Dev import pprint

from mgraph_ai_serverless.graph_engines.graphviz.Graphviz__Render import Graphviz__Render


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