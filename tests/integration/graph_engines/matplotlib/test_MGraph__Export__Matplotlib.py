import networkx as nx
from unittest                                                                   import TestCase
from osbot_utils.utils.Files                                                    import file_create_from_bytes
from mgraph_ai.providers.simple.schemas.Schema__Simple__Node                    import Schema__Simple__Node
from mgraph_ai_serverless.graph_engines.matplotlib.MGraph__Export__Matplotlib   import MGraph__Export__Matplotlib
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.utils.Objects                                                  import __, base_types, obj, type_full_name
from mgraph_ai.mgraph.actions.exporters.MGraph__Export__Base                    import MGraph__Export__Base
from mgraph_ai.providers.simple.MGraph__Simple                                  import MGraph__Simple

class test_MGraph__Export__NetworkX(TestCase):

    def setUp(self):                                                                    # Initialize test environment
        self.mgraph_simple = MGraph__Simple()
        self.exporter     = MGraph__Export__Matplotlib(graph=self.mgraph_simple.graph)

    def test_init(self):                                                                # Test initialization and inheritance
        assert type(self.exporter)        is MGraph__Export__Matplotlib
        assert base_types(self.exporter) == [MGraph__Export__Base, Type_Safe, object]   # Check inheritance chain

    def test_create_node_data(self):                                                    # Test node data creation
        with self.mgraph_simple.edit() as edit:
            node = edit.new_node(value='test_value', name='test_name')

        node_data = self.exporter.create_node_data(node)
        assert obj(node_data) == __( id    = str(node.node_id)               ,          # Check exact structure using __
                                    type  = node.node.data.node_type.__name__,
                                    label = 'test_name'                       )

    def test_create_edge_data(self):                                                    # Test edge data creation
        with self.mgraph_simple.edit() as edit:
            node_1 = edit.new_node(value='test1')
            node_2 = edit.new_node(value='test2')
            edge_1 = edit.new_edge(from_node_id = node_1.node_id,
                                  to_node_id   = node_2.node_id)

        edge_data = self.exporter.create_edge_data(edge_1)
        assert obj(edge_data) == __( id     = str(edge_1.edge_id       )         ,      # Check exact structure using __
                                    source = str(edge_1.from_node_id())         ,
                                    target = str(edge_1.to_node_id  ())         ,
                                    type   = edge_1.edge.data.edge_type.__name__)

    def test_get_node_label(self):                                                      # Test label generation
        with self.mgraph_simple.edit() as edit:
            node_1 = edit.new_node(name='test_name')                                     # Test with name
            assert node_1.obj().node                    == __( data = __( node_data = __( value = None                   ,
                                                                                         name  = 'test_name')           ,
                                                                         node_id   = node_1.node_id                     ,
                                                                         node_type = type_full_name(Schema__Simple__Node)))
            assert self.exporter.get_node_label(node_1) == 'test_name'

            node_2 = edit.new_node(value='test_value')                                  # Test with value but no name
            assert node_2.obj().node                    == __( data = __( node_data = __( value = 'test_value'          ,
                                                                                         name  = None)                  ,
                                                                         node_id   = node_2.node_id                     ,
                                                                         node_type = type_full_name(Schema__Simple__Node)))
            assert self.exporter.get_node_label(node_2) == 'test_value'

            node3 = edit.new_node(name='test_name', value='test_value')                 # Test with both name and value
            assert self.exporter.get_node_label(node3) == 'test_name'

            node4 = edit.new_node()                                                     # Test with neither name nor value
            assert self.exporter.get_node_label(node4) == node4.node.data.node_type.__name__

    def test_to_networkx(self):                                                         # Test NetworkX graph conversion
        with self.mgraph_simple.edit() as edit:
            node_1 = edit.new_node(value='test1')
            node_2 = edit.new_node(value='test2')
            edge_1 = edit.new_edge(from_node_id = node_1.node_id,
                                  to_node_id   = node_2.node_id)

        nx_graph = self.exporter.to_networkx()

        assert type(nx_graph)              is nx.Graph                                  # Check graph type
        assert len(nx_graph.nodes())       == 2                                        # Check node count
        assert len(nx_graph.edges())       == 1                                        # Check edge count

        # Check node attributes
        node_1_id = str(node_1.node_id)
        assert nx_graph.nodes[node_1_id]['type' ] == node_1.node.data.node_type.__name__
        assert nx_graph.nodes[node_1_id]['label'] == 'test1'

        # Check edge attributes
        edge_attrs = next(iter(nx_graph.edges.values()))
        assert edge_attrs['type'] == edge_1.edge.data.edge_type.__name__

    def test_to_image(self):                                                            # Test image generation
        with self.mgraph_simple.edit() as edit:
            node_1 = edit.new_node(value='test1')
            node_2 = edit.new_node(value='test2')
            edge_1 = edit.new_edge(from_node_id = node_1.node_id,
                                  to_node_id   = node_2.node_id)


        # Test different formats and layouts
        layouts = ['spring', 'circular', 'random', 'shell', 'spectral']
        formats = ['png', 'pdf', 'svg']

        for layout in layouts:
            for format in formats:
                image_data = self.exporter.to_image(layout=layout,
                                                    format=format,
                                                    figsize=(8, 8),
                                                    dpi=72)

                assert type(image_data)     is bytes                                      # Check return type
                assert len(image_data)      > 0                                         # Check content exists
                # Verify it's valid base64
                if format == 'png':
                    image_data[0:10].startswith(b'\x89PNG')                              # Check PNG header
                elif format == 'pdf':
                    image_data[0:4].startswith(b'%PDF')                                  # Check PDF header
                elif format == 'svg':
                    image_data[0:5].startswith(b'<?xml vers')                            # Check SVG header
                file_create_from_bytes(f'/tmp/test_image_{layout}.{format}', image_data) # Save image to file

    def test_format_output(self):                                                       # Test output formatting
        with self.mgraph_simple.edit() as edit:
            node_1 = edit.new_node(value='test1')
            node_2 = edit.new_node(value='test2')
            edge_1 = edit.new_edge(from_node_id = node_1.node_id,
                                   to_node_id   = node_2.node_id)

        output = self.exporter.process_graph()

        assert type(output)               is dict                                      # Check main structure
        assert 'nodes'                    in output
        assert 'edges'                    in output

        nodes = output['nodes']
        edges = output['edges']

        assert len(nodes)                  == 2                                         # Check content size
        assert len(edges)                  == 1

        # Check node structure
        node = nodes[0]
        assert 'id'                       in node
        assert 'type'                     in node
        assert 'position'                 in node
        assert 'x'                        in node['position']
        assert 'y'                        in node['position']

        # Check position values are floats
        assert type(node['position']['x']) is float
        assert type(node['position']['y']) is float

# from mgraph_ai.providers.json.MGraph__Json import MGraph__Json
#         mgraph = MGraph__Json()
#         test_data = {"string": "value",
#                           "number": 42,
#                           "boolean": True,
#                           "null": None,
#                           "array": [1, 2, 3],
#                           "object": {"key": "value"}}
#
#         mgraph.load().from_data(test_data)
#         self.exporter = MGraph__Export__Matplotlib(graph=mgraph.graph)