__all__ = [
    'KeyWordArgumentContext',
]

from ._dict import *


class KeyWordArgumentContext(DictContext):
    def __init__(self, **kwargs):
        super().__init__(context_map=kwargs)
