def ensure_browser_is_installed():
    from mgraph_ai_serverless.graph_engines.playwright.Playwright__Serverless import Playwright__Serverless
    playwright_browser = Playwright__Serverless()
    playwright_browser.browser__install()