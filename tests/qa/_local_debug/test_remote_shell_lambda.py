import pytest
from unittest                                                       import TestCase
from osbot_utils.utils.Misc                                         import base64_to_bytes
from mgraph_ai_serverless.utils._for_osbot_aws.Http__Remote_Shell   import Http__Remote_Shell
from osbot_utils.utils.Env                                          import get_env

ENV_VAR_NAME__QA_LAMBDA = 'ENDPOINT_URL__QA_LAMBDA'


@pytest.mark.skip("only used for manual testing")
class test_remote_shell_lambda(TestCase):

    @classmethod
    def setUp(cls):
        cls.port  = 5002
        cls.target_server = get_env(ENV_VAR_NAME__QA_LAMBDA)
        #cls.target_server = "http://localhost:8080"
        cls.target_url = f'{cls.target_server}/debug/lambda-shell'
        cls.shell = Http__Remote_Shell(target_url=cls.target_url)

    def test_0_lambda_shell_setup(self):
        assert self.shell.ping() == 'pong'

    def test_1_matplotlib_render(self):
        def render_graph():
            from mgraph_ai.providers.json.MGraph__Json                                          import MGraph__Json
            from mgraph_ai_serverless.graph_engines.matplotlib.Matplotlib__Render               import Matplotlib__Render
            from mgraph_ai_serverless.graph_engines.matplotlib.models.Model__Matplotlib__Render import Model__Matplotlib__Render
            from osbot_utils.utils.Misc                                                         import bytes_to_base64
            test_data       = {"test-1":"aaaaa-11111","cc":[1,2,3,4,5,6]}
            mgraph_json     = MGraph__Json()
            mgraph_json.load().from_data(test_data)

            matplotlib_render = Model__Matplotlib__Render()
            renderer        = Matplotlib__Render(graph=mgraph_json.graph)
            return {'bytes__base64': bytes_to_base64(renderer.render_graph(matplotlib_render))}

        result = self.shell.function(render_graph)
        #result = render_graph()
        bytes  = base64_to_bytes(result.get('bytes__base64'))
        assert bytes.startswith(b'\x89PNG')
        #file_create_from_bytes('./test.png', bytes)

    def test_2_matplotlib_render__via_Routes__Matplotlib(self):
        def render_graph():
            from mgraph_ai.providers.json.MGraph__Json                                          import MGraph__Json
            from mgraph_ai_serverless.graph_engines.matplotlib.models.Model__Matplotlib__Render import Model__Matplotlib__Render
            from mgraph_ai_serverless.graph_engines.matplotlib.Matplotlib__Render               import Matplotlib__Render
            from osbot_utils.utils.Misc                                                         import bytes_to_base64
            test_data       = {"aa":"bbb","cc":[1,2,3,4,5]}
            mgraph_json     = MGraph__Json()
            mgraph_json.load().from_data(test_data)
            graph_data               = mgraph_json.graph.json()
            model__matplotlib_render = Model__Matplotlib__Render(graph_data=graph_data)
            matplotlib_render        = Matplotlib__Render()
            screenshot_bytes         = matplotlib_render.render_graph(model__matplotlib_render)
            return {'bytes__base64': bytes_to_base64(screenshot_bytes)}


        result = self.shell.function(render_graph)
        bytes  = base64_to_bytes(result.get('bytes__base64'))
        assert bytes.startswith(b'\x89PNG')
        #file_create_from_bytes('./test.png', bytes)




    # examples below were used to fix the bug that happened because the preinstalled Playwright was not being recognised in the Lambda execution environment
    # def test_1_playwright__cli(self):
    #     def playwright__install_chrome():
    #         from osbot_playwright.playwright.api.Playwright_CLI import Playwright_CLI
    #         browser_name = 'chromium'
    #         with Playwright_CLI() as _:
    #             install_status   = _.browser_installed__chrome()
    #             install_location = _.install_details(browser_name).get('install_location')
    #             executable_path  = _.executable_path__chrome()
    #         return dict(install_status   = install_status  ,
    #                     install_location = install_location,
    #                     executable_path  = executable_path )
    #     response = self.shell.function(playwright__install_chrome)
    #     pprint(response)
    #
    # def test_2_playwright__check_docker_install_location(self):
    #     assert self.shell.ls('/root/.cache/ms-playwright/chromium-1148/chrome-linux/chrome') == ''
    #     assert self.shell.ls('/root/.cache/ms-playwright/chromium-1148/chrome-linux'       ) == ''
    #     assert self.shell.ls('/root/.cache/ms-playwright/chromium-1148/'                   ) == ''
    #     assert self.shell.ls('/root/.cache/ms-playwright/'                                 ) == ''
    #     assert self.shell.ls('/root/.cache/'                                               ) == ''
    #     assert self.shell.ls('/root/'                                                      ) == ''


