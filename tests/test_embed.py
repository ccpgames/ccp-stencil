import unittest

from ccpstencil.stencils import *

import sys
import os
import pathlib

_HERE = pathlib.Path(__file__).parent.resolve()


def fp(file_name: str) -> str:
    return str((_HERE / 'res/embed/' / file_name).absolute())


def read_expected(file_name: str) -> str:
    with open(fp(f'expected/{file_name}'), 'r', newline=None) as fin:
        return fin.read()


class TestEmbed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['STENCIL_TEMPLATE_PATH'] = str(_HERE / 'res/embed/')
        os.environ['ENVIRONMENT_VARIABLE_FORTY_TWO'] = '42'

    def test_direct_embed(self):
        # res = render_stencil(fp('template_direct.yaml'), )
        res = render_stencil('template_direct.yaml', fp('context.yaml'))
        exp = read_expected('direct.yaml')
        self.assertEqual(exp, res)

    def test_variable_embed(self):
        res = render_stencil('template_variable.yaml', fp('context.yaml'))
        exp = read_expected('direct.yaml')
        self.assertEqual(exp, res)

    def test_list_embed(self):
        res = render_stencil('template_list.yaml', fp('context.yaml'))
        exp = read_expected('list.yaml')
        self.assertEqual(exp, res)

    def test_alviss_embed(self):
        res = render_stencil('template_alviss.yaml', fp('context.yaml'))
        exp = read_expected('alviss.yaml')
        self.assertEqual(exp, res)

    def test_alviss_embed_with_env(self):
        res = render_stencil('template_alviss_env.yaml', fp('context.yaml'))
        exp = read_expected('alviss_env.yaml')
        self.assertEqual(exp, res)

    @classmethod
    def tearDownClass(cls):
        if 'STENCIL_TEMPLATE_PATH' in os.environ:
            del os.environ['STENCIL_TEMPLATE_PATH']
        if 'ENVIRONMENT_VARIABLE_FORTY_TWO' in os.environ:
            del os.environ['ENVIRONMENT_VARIABLE_FORTY_TWO']
