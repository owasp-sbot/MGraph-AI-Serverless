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

    # def test_2_playwright__executable_path__chrome(self):
    #     def playwright___executable_path__chrome():
    #         from osbot_playwright.playwright.api.Playwright_CLI import Playwright_CLI
    #
    #         Playwright_CLI.executable_path__chrome = lambda _: '/root/.cache/ms-playwright/chromium-1148/chrome-linux/chrome'
    #
    #         with Playwright_CLI() as _:
    #
    #             return _.executable_path__chrome()

    def test_2_playwright__check_docker_install_location(self):
        assert self.shell.ls('/root/.cache/ms-playwright/chromium-1148/chrome-linux/chrome') == '/root/.cache/ms-playwright/chromium-1148/chrome-linux/chrome\n'
        assert self.shell.ls('/root/.cache/ms-playwright/chromium-1148/chrome-linux'       ) == ('MEIPreload\n'
                                                                                                 'PrivacySandboxAttestationsPreloaded\n'
                                                                                                 'chrome\n'
                                                                                                 'chrome-wrapper\n'
                                                                                                 'chrome_100_percent.pak\n'
                                                                                                 'chrome_200_percent.pak\n'
                                                                                                 'chrome_crashpad_handler\n'
                                                                                                 'chrome_sandbox\n'
                                                                                                 'icudtl.dat\n'
                                                                                                 'libEGL.so\n'
                                                                                                 'libGLESv2.so\n'
                                                                                                 'libvk_swiftshader.so\n'
                                                                                                 'libvulkan.so.1\n'
                                                                                                 'locales\n'
                                                                                                 'product_logo_48.png\n'
                                                                                                 'resources\n'
                                                                                                 'resources.pak\n'
                                                                                                 'v8_context_snapshot.bin\n'
                                                                                                 'vk_swiftshader_icd.json\n'
                                                                                                 'xdg-mime\n'
                                                                                                 'xdg-settings\n')
        assert self.shell.ls('/root/.cache/ms-playwright/chromium-1148/'                   ) == 'DEPENDENCIES_VALIDATED\nINSTALLATION_COMPLETE\nchrome-linux\n'
        assert self.shell.ls('/root/.cache/ms-playwright/'                                 ) == 'chromium-1148\nchromium_headless_shell-1148\nffmpeg-1010\n'
        assert self.shell.ls('/root/.cache/'                                               ) == 'ms-playwright\npip\n'
        assert self.shell.ls('/root/'                                                      ) == ''




