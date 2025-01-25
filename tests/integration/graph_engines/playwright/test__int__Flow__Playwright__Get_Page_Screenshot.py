from unittest                                                                                   import TestCase
from mgraph_ai_serverless.graph_engines.playwright.steps.Flow__Playwright__Get_Page_Screenshot  import Flow__Playwright__Get_Page_Screenshot
from osbot_utils.utils.Misc                                                                     import base64_to_bytes
from tests.integration.obj_for_tests__mgraph_ai_serverless                                      import ensure_browser_is_installed


class test__int__Flow__Playwright__Get_Page_Screenshot(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        ensure_browser_is_installed()
        cls.flow__get_page_screenshot = Flow__Playwright__Get_Page_Screenshot()

    def test_run(self):
        flow_data         = self.flow__get_page_screenshot.run()
        screenshot_bytes  = flow_data.get('screenshot_bytes')
        screenshot_base64 = flow_data.get('screenshot_base64')

        assert screenshot_bytes.startswith(b"\x89PNG\r\n\x1a") is True
        assert len(screenshot_bytes )                          > 10000
        assert len(screenshot_base64)                          > 10000
        assert base64_to_bytes(screenshot_base64)              == screenshot_bytes
