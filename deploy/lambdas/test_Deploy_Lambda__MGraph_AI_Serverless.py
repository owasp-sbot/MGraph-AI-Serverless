from unittest                                           import TestCase
from mgraph_ai_serverless.utils.Version                 import version__mgraph_ai_serverless
from deploy.lambdas.Deploy_Lambda__MGraph_AI_Serverless import Deploy_Lambda__MGraph_AI_Serverless


class test_Deploy_Lambda__MGraph_AI_Serverless(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.deploy_lambda = Deploy_Lambda__MGraph_AI_Serverless()

    def test_deploy_lambda(self):
        with self.deploy_lambda as _:
            result = _.lambda_deploy()
            assert result == {'body': 'Hello from Docker Lambda!', 'statusCode': 200}

    def test_ecr_image_uri(self):
        with self.deploy_lambda as _:
            ecr_image_uri = _.ecr_image_uri()       # todo: change values below to aws_config.account_id() and aws_config.region_name()
            assert ecr_image_uri == f'654654216424.dkr.ecr.eu-west-1.amazonaws.com/osbot_flows:{version__mgraph_ai_serverless}'
