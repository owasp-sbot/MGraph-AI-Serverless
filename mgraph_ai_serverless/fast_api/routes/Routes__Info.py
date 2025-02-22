from osbot_fast_api.api.Fast_API_Routes  import Fast_API_Routes
from mgraph_ai_serverless.utils.Version  import version__mgraph_ai_serverless

ROUTES_PATHS__INFO = ['/info/version',  '/info/ping']

class Routes__Info(Fast_API_Routes):
    tag :str = 'info'

    def ping(self):
        return 'pong'

    def version(self):
        return {'version': version__mgraph_ai_serverless}

    
    def setup_routes(self):
        self.add_route_get(self.ping)
        self.add_route_get(self.version)

