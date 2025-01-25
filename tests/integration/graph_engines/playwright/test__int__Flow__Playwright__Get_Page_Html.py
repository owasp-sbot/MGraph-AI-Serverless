from unittest                                                                   import TestCase

from osbot_utils.utils.Dev import pprint

from mgraph_ai_serverless.graph_engines.playwright.steps.Flow__Playwright__Get_Page_Html import \
    Flow__Playwright__Get_Page_Html
from osbot_utils.utils.Misc                                               import list_set
from osbot_utils.helpers.flows.Flow                                       import Flow
from tests.integration.obj_for_tests__mgraph_ai_serverless import ensure_browser_is_installed


class test__int__Flow__Playwright__Get_Page_Html(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        ensure_browser_is_installed()
        cls.flow__get_page_html = Flow__Playwright__Get_Page_Html()

    def test_flow_playwright__get_page_html(self):

        with self.flow__get_page_html.flow_playwright__get_page_html() as _:
            assert type(_) is Flow
            assert _.flow_config.json() == { 'add_task_to_self'       : True,
                                             'log_to_console'         : False,
                                             'log_to_memory'          : True,
                                             'logging_enabled'        : True,
                                             'print_finished_message' : False,
                                             'print_logs'             : False,
                                             'print_none_return_value': False}
            assert _.execute_flow() == _
            _.print_log_messages()
            #assert list_set(_.data) == ['page_content']
            #assert 'Google' in _.data.get('page_content')
