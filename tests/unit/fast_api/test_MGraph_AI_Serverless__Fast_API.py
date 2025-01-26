from unittest import TestCase

from osbot_utils.utils.Files import folder_name, folder_exists

from mgraph_ai_serverless.fast_api.MGraph_AI_Serverless__Fast_API import MGraph_AI_Serverless__Fast_API


class test_MGraph_AI_Serverless__Fast_API(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.fast_api = MGraph_AI_Serverless__Fast_API()

    def test_path_static_folder(self):
        with self.fast_api as _:
            static_folder = _.path_static_folder()
            assert folder_exists(static_folder)
            assert folder_name  (static_folder) == 'web_root'

