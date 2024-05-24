__all__ = [
    'ITemplate',
]
import abc
from typing import *
import jinja2

if TYPE_CHECKING:
    from ._renderer import IRenderer


class ITemplate(abc.ABC):
    @property
    @abc.abstractmethod
    def renderer(self) -> 'IRenderer':
        pass

    @abc.abstractmethod
    def set_renderer(self, renderer: 'IRenderer'):
        pass

    @abc.abstractmethod
    def get_jinja_template(self) -> jinja2.Template:
        pass
