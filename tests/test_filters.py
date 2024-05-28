import unittest

from ccpstencil.stencils import *

import sys
import os
import pathlib

_HERE = pathlib.Path(__file__).parent.resolve()


def fp(file_name: str) -> str:
    return str((_HERE / 'res/filters/' / file_name).absolute())


def read_expected(file_name: str) -> str:
    with open(fp(f'expected/{file_name}'), 'r', newline=None) as fin:
        return fin.read()


class TestFilters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['STENCIL_TEMPLATE_PATH'] = str(_HERE / 'res/filters/')

    def test_base64(self):
        res = render_stencil('base64.yaml', fp('context.yaml'))
        exp = read_expected('base64.yaml')
        self.assertEqual(exp, res)

    @classmethod
    def tearDownClass(cls):
        if 'STENCIL_TEMPLATE_PATH' in os.environ:
            del os.environ['STENCIL_TEMPLATE_PATH']
