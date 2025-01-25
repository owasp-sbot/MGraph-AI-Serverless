from unittest                                                                import TestCase
from mgraph_ai_serverless.graph_engines.playwright.Playwright__Install_Check import Playwright__Install_Check
from osbot_utils.utils.Env                                                   import not_in_github_action




class test_Playwright__Install_Check(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.playwright_chrome_setup = Playwright__Install_Check()

    def test_browser__install_check(self):
        if not_in_github_action():                      # at the moment we only need this locally
            with self.playwright_chrome_setup as _:
                result = _.browser__install_check()
                assert result == { 'chrome__dependencies_validated': True ,
                                   'chrome__installation_complete' : True ,
                                   'ffmpeg__installation_complete' : True ,
                                   'installed_ok'                  : True }
