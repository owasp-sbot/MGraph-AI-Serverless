from unittest                                                                       import TestCase
from starlette.responses                                                            import Response
from mgraph_ai_serverless.graph_engines.graphviz.Graphviz__Render                   import Graphviz__Render
from mgraph_ai_serverless.graph_engines.graphviz.models.Model__Graphviz__Render_Dot import Model__Graphviz__Render_Dot
from mgraph_ai_serverless.graph_engines.graphviz.routes.Routes__Graphviz            import Routes__Graphviz, ROUTES__GRAPHVIZ__RENDER


class test__Routes__Graphviz(TestCase):

    def setUp(self):                                                            # Setup test environment
        self.routes_graphviz                 = Routes__Graphviz()
        self.routes_graphviz.graphviz_render = Graphviz__Render()

    def test_render_dot(self):                                                  # Test DOT rendering
        render_dot_model = Model__Graphviz__Render_Dot()
        with self.routes_graphviz as _:
            response = _.render_dot(render_dot_model)
            assert type(response)                    is Response
            assert len(response.body)                 > 0
            assert response.status_code              == 200
            assert response.headers['content-type']  == 'image/png'   # BUG

    def test_setup_routes(self):                                                # Test route setup
        with self.routes_graphviz as _:
            _.setup_routes()
            assert _.routes_paths() == ROUTES__GRAPHVIZ__RENDER
            assert _.tag == 'graphviz'