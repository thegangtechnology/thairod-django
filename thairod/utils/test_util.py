from unittest.mock import patch

from django.test import TransactionTestCase as TC
from linebot import LineBotApi

from thairod.utils.load_seed import load_seed


class TestCaseNoDB(TC):
    reset_sequences = True
    patch_external = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if cls.patch_external:
            cls.patch_line_bot_api()

    @classmethod
    def patch_line_bot_api(cls):
        line_patch = patch.object(LineBotApi, 'push_message', return_value=None)
        line_patch.__enter__()
        cls.addClassCleanup(line_patch.__exit__, None, None, None)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class TestCase(TestCaseNoDB):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_seed()
