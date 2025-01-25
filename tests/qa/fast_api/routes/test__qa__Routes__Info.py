import pytest
import requests
from unittest                                           import TestCase
from deploy.lambdas.Deploy_Lambda__MGraph_AI_Serverless import Deploy_Lambda__MGraph_AI_Serverless
from osbot_utils.utils.Env                              import not_in_github_action
from mgraph_ai_serverless.utils.Version                 import version__mgraph_ai_serverless



class test__qa__Routes__Info(TestCase):

    @classmethod
    def setUpClass(cls):
        if not_in_github_action():
            import pytest
            pytest.skip("Needs AWS Credentials")
        cls.deploy_lambda   = Deploy_Lambda__MGraph_AI_Serverless()
        cls.lambda_function = cls.deploy_lambda.lambda_function
        cls.lambda_url      = cls.lambda_function.function_url()
        cls.session         = requests.Session()


    def requests_get(self, endpoint, params=None):
        response = self.session.get(f"{self.lambda_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response

    def test_raw_html_live(self):
        if not_in_github_action():
            pytest.skip("This test can only be executed in GH Actions after the deployment of the latest lambda")
        response = self.requests_get('info/version')
        assert response.status_code == 200
        assert response.json() == {'version': version__mgraph_ai_serverless}