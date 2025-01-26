import pytest
from unittest                                                       import TestCase

from osbot_utils.utils.Dev import pprint

from mgraph_ai_serverless.utils._for_osbot_aws.Http__Remote_Shell   import Http__Remote_Shell
from osbot_utils.utils.Env                                          import get_env


@pytest.mark.skip("only used for manual testing")
class test_local_docker__shell_lambda(TestCase):

    @classmethod
    def setUp(cls):
        cls.port  = 5002
        cls.target_server = "http://localhost:8080"
        cls.target_url = f'{cls.target_server}/debug/lambda-shell'
        cls.shell = Http__Remote_Shell(target_url=cls.target_url)

    def test_0_lambda_shell_setup(self):
        assert self.shell.ping() == 'pong'



    def test_1_playwright__cli(self):
        def playwright__install_chrome():
            from osbot_playwright.playwright.api.Playwright_CLI import Playwright_CLI
            browser_name = 'chromium'
            with Playwright_CLI() as _:
                install_status   = _.browser_installed__chrome()
                install_location = _.install_details(browser_name).get('install_location')
                executable_path  = _.executable_path__chrome()
            return dict(install_status   = install_status  ,
                        install_location = install_location,
                        executable_path  = executable_path )
        response = self.shell.function(playwright__install_chrome)
        pprint(response)
        # { 'install_location': '/tmp/osbot_playwright_browsers/chromium-1148',
        #   'install_status': False}

    def test_2_playwright__executable_path__chrome(self):
        def playwright___executable_path__chrome():
            from osbot_playwright.playwright.api.Playwright_CLI import Playwright_CLI

            Playwright_CLI.executable_path__chrome = lambda _: '/root/.cache/ms-playwright/chromium-1148/chrome-linux/chrome'

            with Playwright_CLI() as _:

                return _.executable_path__chrome()

        #response = self.shell.function(playwright___executable_path__chrome)

        #response = self.shell.ls('/root/.cache/ms-playwright/chromium-1148/chrome-linux/chrome')
        response = self.shell.ls('/tmp/osbot_playwright_browsers/chromium-1148')
        pprint(response)



