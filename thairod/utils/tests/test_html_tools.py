from unittest import TestCase

from thairod.utils import html_tools as ht


class HTMLToolsTest(TestCase):
    with_db = False

    def test_get_body(self):
        s = """
        <html>
            <head>
            </head>
            <body>
                hello
            </body>
        </html>
        """
        assert ht.get_body(s).strip() == "hello"
