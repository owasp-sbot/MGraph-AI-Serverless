from osbot_utils.utils.Json                                                                     import json_dumps
from osbot_utils.utils.Http                                                                     import url_join_safe
from mgraph_ai_serverless.graph_engines.playwright.flows.Flow__Playwright__Get_Page_Screenshot  import Flow__Playwright__Get_Page_Screenshot
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe

URL__LOCAL_SERVER = 'http://localhost:8080/static'


class Web_Root__Render(Type_Safe):
    target_server = URL__LOCAL_SERVER

    def render_page(self, target_url, js_code=None, wait_for=0):
        with Flow__Playwright__Get_Page_Screenshot() as _:
            _.url      = target_url
            _.js_code  = js_code
            _.wait_for = wait_for
            run_data   = _.run()
            return run_data

    def render__cytoscape(self, cytoscape_data):
        cytoscape_json = json_dumps(cytoscape_data)                         # Convert the Python dict to a JSON string
        js_code          = f"updateGraph({cytoscape_json});"                     # Create JavaScript code to update the graph
        target_url       = self.target_url('cytoscape/index.html')
        run_data         = self.render_page(target_url, js_code=js_code, wait_for=0.5)
        screenshot_bytes = run_data.get('screenshot_bytes')
        return screenshot_bytes

    def render__mermaid(self, mermaid_code):
        js_code = f"""
                    new_graph = `{mermaid_code}`
                    document.querySelector('.mermaid').innerHTML = new_graph
                        document.querySelector('.mermaid').removeAttribute('data-processed');
                    
                    mermaid.init(undefined, ".mermaid");
                    """

        target_url       = self.target_url('mermaid/index.html')
        run_data         = self.render_page(target_url, js_code=js_code)
        screenshot_bytes = run_data.get('screenshot_bytes')
        return screenshot_bytes

    def target_url(self, target_page='examples/hello-world.html'):
        return url_join_safe(self.target_server, target_page)