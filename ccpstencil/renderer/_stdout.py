__all__ = [
    'StdOutRenderer',
]

from ccpstencil.structs import *
from ._string import *


class StdOutRenderer(StringRenderer):
    def render(self) -> NoReturn:
        results = super().render()
        if results is not None:
            print(results)
