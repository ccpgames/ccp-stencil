import unittest

from ccpstencil.stencils import *


class TestSomeBasicStuff(unittest.TestCase):
    def test_basic_stuff(self):
        context = DictContext({
            'name': 'Bob',
            'age': 42,
            'colors': {
                'favorite': 'Red',
                'weakness': 'Yellow'
            }
        })
        template = StringTemplate("My name is {{name}} and I am {{age}} years old and my favorite color"
                                  " is {{colors.favorite}} but I'm allergic to {{colors.weakness}}!")

        renderer = StringRenderer(context, template)

        self.assertEqual(
            "My name is Bob and I am 42 years old and my favorite color"
            " is Red but I'm allergic to Yellow!", renderer.render()
        )

        renderer.context.nested_update('colors.favorite', 'Blue')

        self.assertEqual(
            "My name is Bob and I am 42 years old and my favorite color"
            " is Blue but I'm allergic to Yellow!", renderer.render()
        )

