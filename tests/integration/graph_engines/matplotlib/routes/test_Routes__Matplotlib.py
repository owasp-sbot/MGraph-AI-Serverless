from unittest                                                                          import TestCase
from fastapi                                                                           import Response
from mgraph_ai.providers.simple.MGraph__Simple__Test_Data                              import MGraph__Simple__Test_Data
from mgraph_ai_serverless.graph_engines.matplotlib.models.Model__Matplotlib__Render    import Model__Matplotlib__Render
from mgraph_ai_serverless.graph_engines.matplotlib.routes.Routes__Matplotlib           import Routes__Matplotlib


class test_Routes__Matplotlib(TestCase):

    @classmethod
    def setUpClass(cls):                                                               # Setup test environment
        cls.test_graph = MGraph__Simple__Test_Data().create()
        cls.routes    = Routes__Matplotlib()

    def setUp(self):
        self.render_config = Model__Matplotlib__Render(graph_data = self.test_graph.graph.json()) # Default render config with graph data

    def test_init(self):                                                            # Test initialization
        assert type(self.routes)        is Routes__Matplotlib
        assert 'matplotlib'             == self.routes.tag

    def test_render_graph_direct(self):                                             # Test direct method call
        response = self.routes.render_graph(self.render_config)

        assert isinstance(response, Response)
        assert response.media_type == 'image/png'
        assert len(response.body) > 0
        assert response.body.startswith(b'\x89PNG')                                 # Verify PNG header

    def test_render_graph_different_formats(self):                                 # Test different output formats
        formats = ['png', 'svg', 'pdf']
        for format in formats:
            render_config = self.render_config
            render_config.output_format = format

            response = self.routes.render_graph(render_config)

            assert isinstance(response, Response)
            assert response.media_type == f'image/{format}'
            assert len(response.body) > 0

    def test_render_graph_different_layouts(self):                                # Test different layout algorithms
        layouts = ['spring', 'circular', 'random', 'shell', 'spectral']
        for layout in layouts:
            render_config = self.render_config
            render_config.layout = layout

            response = self.routes.render_graph(render_config)

            assert isinstance(response, Response)
            assert len(response.body) > 0

