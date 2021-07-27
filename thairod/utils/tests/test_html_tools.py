from unittest import TestCase

from thairod.utils import html_tools as ht


class HTMLToolsTest(TestCase):

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
        print(repr(ht.get_body(s).strip()))
        assert ht.get_body(s).strip() == "hello"
