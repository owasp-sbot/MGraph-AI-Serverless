from unittest                                                                               import TestCase
from mgraph_ai.providers.simple.MGraph__Simple                                              import MGraph__Simple
from mgraph_ai_serverless.graph_engines.matplotlib.Matplotlib__Render                       import Matplotlib__Render
from mgraph_ai_serverless.graph_engines.matplotlib.models.Model__Matplotlib__Render         import Model__Matplotlib__Render
from mgraph_ai_serverless.graph_engines.matplotlib.models.Model__Matplotlib__Output_Format  import Model__Matplotlib__Output_Format
from osbot_utils.utils.Objects                                                              import base_types
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe

# refactor/merge this with the tests in test__int__Matplotlib__Render.py

class test_Matplotlib__Render(TestCase):

    def setUp(self):                                                                    # Set up test graph
        self.mgraph_simple = MGraph__Simple()
        self.renderer      = Matplotlib__Render()

        with self.mgraph_simple.edit() as edit:                                          # Create a simple test graph
            self.node1 = edit.new_node(value='Node 1')
            self.node2 = edit.new_node(value='Node 2')
            self.edge = edit.new_edge(from_node_id=self.node1.node_id,
                                      to_node_id=self.node2.node_id)

        self.graph_data    = self.mgraph_simple.graph.json()
        self.render_config = Model__Matplotlib__Render( graph_data    = self.graph_data,
                                                        layout        = 'spring'       ,
                                                        figsize       = (8, 8)         ,
                                                        node_size     = 500            ,
                                                        node_color    = 'lightblue'    ,
                                                        output_format = Model__Matplotlib__Output_Format.png,
                                                        dpi           = 72                                  )

    def test_init(self):                                                               # Test initialization
        assert type(self.renderer)        is Matplotlib__Render
        assert base_types(self.renderer) == [Type_Safe, object]


    def test_render_graph(self):                                                       # Test graph rendering

        with self.renderer as _:
            image_data = self.renderer.render_graph(self.render_config)

        assert type(image_data) is bytes                                               # Check output type
        assert len(image_data) > 0                                                     # Check content exists
        assert image_data.startswith(b'\x89PNG')                                       # Check PNG header

        #file_create_from_bytes(f'./test_render.png', image_data)

        # Test different formats
        for format in Model__Matplotlib__Output_Format:
            self.render_config.output_format = format
            image_data = self.renderer.render_graph(self.render_config)

            assert type(image_data) is bytes
            assert len(image_data) > 0
            if format == Model__Matplotlib__Output_Format.png:
                assert image_data.startswith(b'\x89PNG')
            elif format == Model__Matplotlib__Output_Format.svg:
                assert image_data.startswith(b'<?xml vers')
            elif format == Model__Matplotlib__Output_Format.pdf:
                assert image_data.startswith(b'%PDF-1.4')

            # # Save test output
            # file_create_from_bytes(f'/tmp/test_render.{format.value}', image_data)

    def test_create_image(self):                                                      # Test graph processing
        with self.renderer as _:
            graph_data = self.render_config.graph_data
            graph      = _.create_graph_from_graph_data(graph_data)
            output     = self.renderer.create_image   (self.render_config, graph)

        assert type(output) is bytes                                                    # Check structure
        assert output.startswith(b'\x89PNG')