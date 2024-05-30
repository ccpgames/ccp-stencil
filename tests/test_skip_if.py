import unittest

from ccpstencil.stencils import *

import os
import pathlib

import logging
logging.basicConfig(level=logging.DEBUG)


_HERE = pathlib.Path(__file__).parent.resolve()


def fp(file_name: str) -> str:
    return str((_HERE / 'res/skipif/' / file_name).absolute())


class TestSkipIf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['STENCIL_TEMPLATE_PATH'] = str(_HERE / 'res/skipif/')

    def test_normal(self):
        res = render_stencil('template_normal.txt', fp('context.yaml'))
        self.assertEqual('The day is Now', res)

    def test_skipped(self):
        res = render_stencil('template_negative.txt', fp('context.yaml'))
        self.assertIsNone(res)

    def test_not_skipped(self):
        res = render_stencil('template_positive.txt', fp('context.yaml'))
        self.assertEqual('The day is Shiny', res)

    def test_numbers(self):
        # res = render_stencil('template_six.txt', fp('context.yaml'))
        # self.assertEqual('Six!', res)
        res = render_stencil('template_seven.txt', fp('context.yaml'))
        self.assertIsNone(res)

    @classmethod
    def tearDownClass(cls):
        if 'STENCIL_TEMPLATE_PATH' in os.environ:
            del os.environ['STENCIL_TEMPLATE_PATH']
