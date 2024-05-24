__all__ = [
    'StdOutRenderer',
]


from ._string import *


class StdOutRenderer(StringRenderer):
    def render(self):
        print(super().render())
