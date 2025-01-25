from unittest                                                   import TestCase

import pytest
from playwright.async_api._generated                                      import Clock, BrowserContext, Keyboard, Mouse, Touchscreen, APIRequestContext
from mgraph_ai_serverless.graph_engines.playwright.Playwright__Serverless import Playwright__Serverless
from osbot_utils.utils.Misc                                               import list_set
from playwright.async_api                                                 import Playwright, Browser, Response, Request, Frame, Page, Accessibility
from osbot_utils.utils.Threads                                            import async_invoke_in_new_loop, invoke_async
from osbot_utils.utils.Env                                                import in_github_action, not_in_github_action
from osbot_utils.utils.Files                                              import file_name, file_exists, folder_exists, folder_name

class test_Playwright__Serverless(TestCase):

    def setUp(self) -> None:
        self.playwright__serverless = Playwright__Serverless()


    def test__init__(self):
        with self.playwright__serverless as _:
            expected_locals = dict(browser        = None             ,
                                   page           = None             ,
                                   playwright     = None             ,
                                   playwright_cli = _.playwright_cli ,
                                   response       = None             ,
                                   screenshot     = None             )

            assert self.playwright__serverless.__locals__() == expected_locals

    def test_1__browser__install(self):                                         # (first test to be executed) make sure that the browser is installed
        with self.playwright__serverless as _:
            assert _.browser__install() is True

    def test_launch(self):
        with self.playwright__serverless as _:
            browser = async_invoke_in_new_loop(_.launch())
            assert type(browser) is Browser

    def test_browser__exists(self):
        with self.playwright__serverless as _:
            assert _.browser__exists() is True

    def test_chrome_path(self):
        with self.playwright__serverless as _:
            chrome_path = _.chrome_path()
            assert file_exists(chrome_path)
            if in_github_action():
                assert file_name(chrome_path) == 'chrome'
            else:
                assert file_name(chrome_path) == 'Chromium'

    @pytest.mark.skip("See if this has an impact on the GH Actions event loop warnings")
    def test_goto(self):
        async def get_response(url):
            with self.playwright__serverless as _:
                await _.new_page()
                return await _.goto(url)

        url             = "https://www.google.com/"
        response        = invoke_async(get_response(url))
        frame           = response.frame
        headers         = response.headers
        ok              = response.ok
        request         = response.request
        status          = response.status
        url             = response.url
        page            = frame.page
        accessibility   = page.accessibility
        clock           = page.clock
        context         = page.context
        frames          = page.frames
        keyboard        = page.keyboard
        main_frame      = page.main_frame
        request_context = page.request
        mouse           = page.mouse
        touchscreen     = page.touchscreen

        assert type(response       ) is Response
        assert type(frame          ) is Frame
        assert type(headers        ) is dict
        assert type(ok             ) is bool
        assert type(request        ) is Request
        assert type(status         ) is int
        assert type(url            ) is str
        assert type(page           ) is Page
        assert type(accessibility  ) is Accessibility
        assert type(clock          ) is Clock
        assert type(context        ) is BrowserContext
        assert type(keyboard       ) is Keyboard
        assert type(mouse          ) is Mouse
        assert type(request_context) is APIRequestContext
        assert type(touchscreen    ) is Touchscreen

        assert response.url           == url
        assert type(response.request) == Request
        assert list_set(headers)      == [ 'accept-ch',  'alt-svc', 'cache-control', 'content-encoding',
                                           'content-length', 'content-security-policy-report-only', 'content-type',
                                           'cross-origin-opener-policy', 'date', 'expires', 'p3p', 'permissions-policy',
                                           'report-to', 'server', 'x-frame-options', 'x-xss-protection']
        if not_in_github_action():
            assert frame.child_frames == []         # there was an extra frame here when running in GH Actions (a 'callout')
            assert frames             == [frame]
        assert frame.parent_frame     is None
        assert frame.name             == ''
        assert frame.url              == url
        assert ok                     is True
        assert status                 == 200
        assert main_frame             == frame
        assert page.url               == url
        assert page.video             is None
        assert page.viewport_size     == {'width': 1280, 'height': 720}

        # todo: see what other properties we can assert

    def test_screenshot_bytes(self):
        async def get_screenshot_bytes(url):
            with self.playwright__serverless as _:
                await _.new_page()
                await _.goto(url)
                return await _.screenshot_bytes()

        screenshot_bytes = invoke_async(get_screenshot_bytes("https://www.google.com/"))
        assert screenshot_bytes.startswith(b'\x89PNG')

    def test_start(self):
        with self.playwright__serverless as _:
            playwright = async_invoke_in_new_loop(_.start())
            assert type(playwright) is Playwright
            assert _.playwright == playwright

    def test_stop(self):
        async def start_and_stop():
            with self.playwright__serverless as _:
                await _.start()
                await _.stop()
        invoke_async(start_and_stop())

    # ----------

    # def test_run_playwright_in_pytest(self):
    #     from osbot_utils.utils.Threads                       import async_invoke_in_new_loop
    #     from osbot_utils.utils.Misc                          import bytes_to_base64
    #     from playwright.async_api                            import async_playwright
    #     from osbot_playwright.playwright.api.Playwright_CLI import Playwright_CLI
    #     playwright_cli = Playwright_CLI()
    #     chrome_path    = playwright_cli.executable_path__chrome()
    #
    #     async def get_screenshot(url):
    #
    #         playwright        = await async_playwright().start()
    #         launch_kwargs = dict(args=["--disable-gpu", "--single-process"],
    #                              executable_path=chrome_path)
    #         browser = await playwright.chromium.launch(**launch_kwargs)
    #
    #         page = await browser.new_page()
    #         await page.goto(url)
    #
    #         screenshot = await page.screenshot(full_page=True)
    #         await playwright.stop()
    #
    #         return bytes_to_base64(screenshot)
    #
    #     async_invoke_in_new_loop(get_screenshot("https://www.google.com/404"))

