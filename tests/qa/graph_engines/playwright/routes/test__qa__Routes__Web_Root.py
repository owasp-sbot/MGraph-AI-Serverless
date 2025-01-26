from unittest import TestCase

import pytest
import requests

from mgraph_ai.providers.json.MGraph__Json  import MGraph__Json
from osbot_utils.utils.Files                import file_create_from_bytes
from osbot_utils.utils.Http                 import url_join_safe
from osbot_utils.utils.Env                  import get_env, load_dotenv
ENV_VAR_NAME__QA_LAMBDA = 'ENDPOINT_URL__QA_LAMBDA'



class test__qa__Routes__Web_Root(TestCase):

    @classmethod
    def setUp(cls):
        load_dotenv()
        cls.target_server = get_env(ENV_VAR_NAME__QA_LAMBDA)
        if not cls.target_server:
            pytest.skip(f"{ENV_VAR_NAME__QA_LAMBDA} env var not set")

    def get_url(self, path):
        return url_join_safe(self.target_server, path)


    def test__1__web_root__render_file(self):
        target_url        = self.get_url('/web_root/render-file')
        response          = requests.get(target_url)
        screenshot_bytes  = response.content
        assert response.status_code                    == 200
        assert screenshot_bytes.startswith(b'\x89PNG') is True

    def test__2__web_root__render_js(self):
        target_url = self.get_url('/web_root/render-js')
        response = requests.get(target_url)
        screenshot_bytes = response.content
        assert response.status_code == 200
        assert screenshot_bytes.startswith(b'\x89PNG') is True

    def test__3__web_root__render_mermaid(self):
        target_url = self.get_url('/web_root/render-mermaid')
        response = requests.post(target_url, json={})
        screenshot_bytes = response.content
        assert response.status_code == 200
        assert screenshot_bytes.startswith(b'\x89PNG') is True

    def test__4__web_root__render_mermaid__mgraph_json(self):
        test_data = { "string" : "value"           ,
                      "number" : 42                ,
                      "boolean": True              ,
                      "null"   : None              ,
                      "array"  : [1, 2, 3]         ,
                      "object" : {"key": "value"   }}

        mgraph_json     = MGraph__Json()

        mgraph_json.load().from_json(test_data)
        mermaid_code    = mgraph_json.export().to__mermaid().to_string()

        target_url       = self.get_url('/web_root/render-mermaid')
        response         = requests.post(target_url, json={ 'mermaid_code': mermaid_code })
        screenshot_bytes = response.content

        assert response.status_code                    == 200
        assert screenshot_bytes.startswith(b'\x89PNG') is True

        #file_create_from_bytes('/tmp/screenshot.png', screenshot_bytes)





