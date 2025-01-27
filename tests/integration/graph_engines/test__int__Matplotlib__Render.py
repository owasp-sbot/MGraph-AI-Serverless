from unittest                                                                          import TestCase
from mgraph_ai.providers.json.MGraph__Json                                             import MGraph__Json
from mgraph_ai.providers.simple.MGraph__Simple__Test_Data                              import MGraph__Simple__Test_Data
from mgraph_ai_serverless.graph_engines.matplotlib.Matplotlib__Render                   import Matplotlib__Render
from mgraph_ai_serverless.graph_engines.matplotlib.models.Model__Matplotlib__Render     import Model__Matplotlib__Render


class test__int__Matplotlib__Render(TestCase):

    @classmethod
    def setUpClass(cls):                                                        # Setup test data
        cls.matplotlib_render = Matplotlib__Render()
        cls.test_graph       = MGraph__Simple__Test_Data().create()

    def test_render_graph(self):                                                # Test rendering with simple test data
        with self.matplotlib_render as _:
            _.graph = self.test_graph.graph                                     # Set the graph to render
            render_config = Model__Matplotlib__Render(
                layout='spring',
                figsize=(10, 10),
                node_size=1000,
                node_color='lightblue'
            )
            result = _.render_graph(render_config)
            assert isinstance(result, bytes)
            assert len(result) > 0
            assert result.startswith(b'\x89PNG')                                # Verify PNG header

    def test_render_graph__json(self):                                         # Test with JSON data
        mgraph    = MGraph__Json()
        test_data = { "string" : "value"         ,
                      "number" : 42              ,
                      "boolean": True            ,
                      "null"   : None            ,
                      "array"  : [1, 2, 3]       ,
                      "object" : {"key": "value"}}

        mgraph.load().from_data(test_data)

        with self.matplotlib_render as _:
            _.graph = mgraph.graph                                              # Set JSON graph for rendering
            render_config = Model__Matplotlib__Render(
                layout='circular',                                              # Use different layout for JSON
                figsize=(12, 12),
                node_size=800,
                node_color='lightgreen'
            )
            result = _.render_graph(render_config)
            assert isinstance(result, bytes)
            assert len(result) > 0
            assert result.startswith(b'\x89PNG')                                # Verify PNG header

    def test_process_graph(self):                                              # Test graph data processing
        with self.matplotlib_render as _:
            _.graph = self.test_graph.graph
            result = _.process_graph()

            assert isinstance(result, dict)
            assert 'nodes' in result
            assert 'edges' in result

            # Verify node positions
            for node in result['nodes']:
                assert 'position' in node
                assert 'x' in node['position']
                assert 'y' in node['position']
                assert isinstance(node['position']['x'], float)
                assert isinstance(node['position']['y'], float)

    def test_render_multiple_formats(self):                                    # Test different output formats
        with self.matplotlib_render as _:
            _.graph = self.test_graph.graph
            formats = ['png', 'svg', 'pdf']

            for format in formats:
                render_config = Model__Matplotlib__Render(
                    layout='spring',
                    output_format=format
                )
                result = _.render_graph(render_config)
                assert isinstance(result, bytes)
                assert len(result) > 0

                # Verify format-specific headers
                if format == 'png':
                    assert result.startswith(b'\x89PNG')
                elif format == 'pdf':
                    assert result.startswith(b'%PDF')
                elif format == 'svg':
                    assert result.startswith(b'<?xml')