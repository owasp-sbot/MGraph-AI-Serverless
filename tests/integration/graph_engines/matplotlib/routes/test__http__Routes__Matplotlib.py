from dataclasses                                                                        import asdict
from unittest                                                                           import TestCase
from osbot_fast_api.utils.Fast_API_Server                                               import Fast_API_Server
from mgraph_ai.providers.simple.MGraph__Simple__Test_Data                               import MGraph__Simple__Test_Data
from mgraph_ai_serverless.testing.mgraph_ai_serverless__objs_for_tests                  import mgraph_ai_serverless__fast_api__app
from mgraph_ai_serverless.graph_engines.matplotlib.models.Model__Matplotlib__Render     import Model__Matplotlib__Render


class test__http__Routes__Matplotlib(TestCase):

    @classmethod
    def setUpClass(cls):                                                        # Start server
        cls.fast_api_server = Fast_API_Server(app=mgraph_ai_serverless__fast_api__app)
        cls.fast_api_server.start()
        assert cls.fast_api_server.is_port_open() is True
        cls.test_graph = MGraph__Simple__Test_Data().create()                   # Create test graph

    @classmethod
    def tearDownClass(cls):                                                     # Stop server
        cls.fast_api_server.stop()
        assert cls.fast_api_server.is_port_open() is False

    def test_http__render_graph(self):                                         # Test basic graph rendering
        render_config = Model__Matplotlib__Render(graph_data       = self.test_graph.graph.json())
        response      = self.fast_api_server.requests_post('/matplotlib/render-graph',data=asdict(render_config))

        assert response.status_code == 200
        assert response.headers['content-type'] == 'image/png'
        assert len(response.content) > 0
        assert response.content.startswith(b'\x89PNG')                         # Verify PNG header
        #file_create_from_bytes('/tmp/test_render.png', response.content)      # Save test output

    def test_http__render_graph_formats(self):                                # Test different formats
        formats = ['png', 'svg', 'pdf']
        for format in formats:
            render_config = Model__Matplotlib__Render(graph_data    = self.test_graph.graph.json(),
                                                      output_format = format                     )

            response = self.fast_api_server.requests_post('/matplotlib/render-graph', data=asdict(render_config))

            assert response.status_code == 200
            assert response.headers['content-type'] == f'image/{format}'
            assert len(response.content) > 0

    def test_http__render_graph_layouts(self):                               # Test different layouts
        layouts = ['spring', 'circular', 'random', 'shell', 'spectral']
        for layout in layouts:
            render_config = Model__Matplotlib__Render(graph_data = self.test_graph.graph.json(),
                                                      layout     = layout                      )

            response = self.fast_api_server.requests_post('/matplotlib/render-graph', data=asdict(render_config))

            assert response.status_code == 200
            assert response.headers['content-type'] == 'image/png'
            assert len(response.content) > 0

    def test_http__render_graph_errors(self):                               # Test error cases
        # Test invalid domain type
        graph_data    = MGraph__Simple__Test_Data().graph.json()
        render_config = Model__Matplotlib__Render(graph_data=graph_data)
        json_data     = asdict(render_config)

        json_data['graph_data']['graph_type'] = 'InvalidDomainType'
        response = self.fast_api_server.requests_post('/matplotlib/render-graph', data=json_data)
        assert response.status_code == 400
        assert response.json()['detail'] == 'Unsupported domain type: InvalidDomainType'

        # No graph provided
        json_data['graph_data'] = {}
        response = self.fast_api_server.requests_post('/matplotlib/render-graph', data=json_data)
        assert response.status_code == 400
        assert response.json()['detail'] == 'No graph provided for rendering'