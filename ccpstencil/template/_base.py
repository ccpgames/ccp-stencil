__all__ = [
    '_BaseTemplate',
]
from ccpstencil.structs import *


class _BaseTemplate(ITemplate, abc.ABC):
    def __init__(self, **kwargs):
        self._renderer: Optional[IRenderer] = None

    @property
    def renderer(self) -> IRenderer:
        return self._renderer

    def set_renderer(self, renderer: IRenderer):
        self._renderer = renderer
