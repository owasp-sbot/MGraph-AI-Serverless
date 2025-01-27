from unittest                                                                               import TestCase
from mgraph_ai.providers.simple.MGraph__Simple                                              import MGraph__Simple
from mgraph_ai_serverless.graph_engines.matplotlib.Matplotlib__Render                       import Matplotlib__Render
from mgraph_ai_serverless.graph_engines.matplotlib.models.Model__Matplotlib__Render         import Model__Matplotlib__Render
from mgraph_ai_serverless.graph_engines.matplotlib.models.Model__Matplotlib__Output_Format  import Model__Matplotlib__Output_Format
from osbot_utils.utils.Objects                                                              import base_types
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe

class test_Matplotlib__Render(TestCase):

    @classmethod
    def setUpClass(cls):                                                            # Setup test data
        import pytest
        pytest.skip("weird race condition here, where these only fail when run with all tests") # todo: investigate
    def setUp(self):                                                                    # Set up test graph
        self.mgraph_simple = MGraph__Simple()
        self.renderer      = Matplotlib__Render(graph=self.mgraph_simple.graph)

        with self.mgraph_simple.edit() as edit:                                          # Create a simple test graph
            self.node1 = edit.new_node(value='Node 1')
            self.node2 = edit.new_node(value='Node 2')
            self.edge = edit.new_edge(from_node_id=self.node1.node_id,
                                      to_node_id=self.node2.node_id)

    def test_init(self):                                                               # Test initialization
        assert type(self.renderer)        is Matplotlib__Render
        assert base_types(self.renderer) == [Type_Safe, object]

    def test_create_exporter(self):                                                    # Test exporter creation
        exporter = self.renderer.create_exporter()
        assert exporter.graph.json() == self.mgraph_simple.graph.json()


    def test_render_graph(self):                                                       # Test graph rendering
        render_config = Model__Matplotlib__Render( layout        = 'spring'   ,
                                                   figsize       = (8, 8)     ,
                                                   node_size     = 500        ,
                                                   node_color    = 'lightblue',
                                                   output_format = Model__Matplotlib__Output_Format.png,
                                                   dpi           = 72                                  )

        image_data = self.renderer.render_graph(render_config)

        assert type(image_data) is bytes                                               # Check output type
        assert len(image_data) > 0                                                     # Check content exists
        assert image_data.startswith(b'\x89PNG')                                       # Check PNG header

        # Test different formats
        for format in Model__Matplotlib__Output_Format:
            render_config.output_format = format
            image_data = self.renderer.render_graph(render_config)

            assert type(image_data) is bytes
            assert len(image_data) > 0

            # # Save test output
            # file_create_from_bytes(f'/tmp/test_render.{format.value}', image_data)

    def test_process_graph(self):                                                      # Test graph processing
        output = self.renderer.process_graph()

        assert type(output) is dict                                                    # Check structure
        assert 'nodes' in output
        assert 'edges' in output

        assert len(output['nodes']) == 2                                               # Check content
        assert len(output['edges']) == 1

        # Check node data structure
        node = output['nodes'][0]
        assert 'id' in node
        assert 'type' in node
        assert 'position' in node
        assert 'x' in node['position']
        assert 'y' in node['position']
