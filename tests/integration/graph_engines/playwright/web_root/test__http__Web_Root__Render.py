from unittest                                                                   import TestCase
from osbot_utils.utils.Files                                                    import save_bytes_as_file, file_exists, file_delete
from mgraph_ai.providers.json.MGraph__Json                                      import MGraph__Json
from osbot_utils.utils.Http                                                     import url_join_safe
from mgraph_ai_serverless.testing.mgraph_ai_serverless__objs_for_tests          import mgraph_ai_serverless__fast_api__app
from osbot_fast_api.utils.Fast_API_Server                                       import Fast_API_Server
from mgraph_ai_serverless.graph_engines.playwright.web_root.Web_Root__Render    import Web_Root__Render


class test_Web_Root__Render(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.web_root_render = Web_Root__Render()
        cls.fast_api_server = Fast_API_Server(app=mgraph_ai_serverless__fast_api__app)
        cls.fast_api_server.start()
        assert cls.fast_api_server.is_port_open() is True

    @classmethod
    def tearDownClass(cls):
        cls.fast_api_server.stop()
        assert cls.fast_api_server.is_port_open() is False

    def target_url(self, target_path):
        target_server = self.fast_api_server.url()
        target_url    = url_join_safe(target_server, target_path)
        return target_url

    def test_render_page(self):
        with self.web_root_render as _:
            target_port      = self.fast_api_server.port
            target_url       = self.target_url('static/examples/hello-world.html')
            response         = _.render_page(target_url)
            screenshot_bytes = response.get('screenshot_bytes')
            assert target_url == f"http://127.0.0.1:{target_port}/static/examples/hello-world.html"
            assert screenshot_bytes.startswith(b'\x89PNG') is True

    def test_render_page__with_js(self):
        with self.web_root_render as _:
            js_code          = """
                                    document.body.style.backgroundColor = "black";
                                    document.body.style.color           = "white";
                                    document.body.innerHTML = '<h1>Dynamic JS</h1>';
                               """
            target_url       = self.target_url('static/examples/hello-world.html')
            response         = _.render_page(target_url, js_code)
            screenshot_bytes = response.get('screenshot_bytes')
            assert screenshot_bytes.startswith(b'\x89PNG') is True
            #save_bytes_as_file(screenshot_bytes, '/tmp/hello-world.png')

    def test_render_mermaid(self):
        test_data = { "string" : "value"         ,
                           "number" : 42                ,
                           "boolean": True              ,
                           "null"   : None              ,
                           "array"  : [1, 2, 3]         ,
                           "object" : {"key": "value"}}

        with MGraph__Json() as _:
            _.load().from_json(test_data)
            mermaid_code = _.export().to__mermaid().to_string()

        with self.web_root_render as _:
            target_file = '/tmp/mermaid.png'
            _.target_server = f'http://localhost:{self.fast_api_server.port}/static'
            screenshot_bytes = _.render__mermaid(mermaid_code)
            assert screenshot_bytes.startswith(b'\x89PNG') is True
            save_bytes_as_file(screenshot_bytes, target_file)
            assert file_exists(target_file) is True
            assert file_delete(target_file) is True


    def test_render__mgraph__json__mermaid(self):                                     # Test with JSON data
        mgraph    = MGraph__Json()
        test_data = { "string" : "value"         ,
                      "number" : 42              ,
                      "boolean": True            ,
                      "null"   : None            ,
                      "array"  : [1, 2, 3]       ,
                      "object" : {"key": "value"}}

        mgraph.load().from_json(test_data)
        dot_text = mgraph.export().to_dot().to_string()

        # with self.graphviz_render as _:
        #     render_config = Model__Graphviz__Render_Dot(dot_source=dot_text)
        #     result = _.render_dot(render_config)
        #     assert isinstance(result, bytes)
        #     assert len(result) > 0

