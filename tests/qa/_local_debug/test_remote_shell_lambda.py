import pytest
from unittest                                                       import TestCase
from mgraph_ai_serverless.utils._for_osbot_aws.Http__Remote_Shell   import Http__Remote_Shell
from osbot_utils.utils.Env                                          import get_env

ENV_VAR_NAME__QA_LAMBDA = 'ENDPOINT_URL__QA_LAMBDA'


@pytest.mark.skip("only used for manual testing")
class test_remote_shell_lambda(TestCase):

    @classmethod
    def setUp(cls):
        cls.port  = 5002
        cls.target_server = get_env(ENV_VAR_NAME__QA_LAMBDA)
        #cls.target_server = "http://localhost:8080"
        cls.target_url = f'{cls.target_server}/debug/lambda-shell'
        cls.shell = Http__Remote_Shell(target_url=cls.target_url)

    def test_0_lambda_shell_setup(self):
        assert self.shell.ping() == 'pong'