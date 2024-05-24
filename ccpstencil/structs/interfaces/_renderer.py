__all__ = [
    'IRenderer',
]
from ccptools.structs import *
from ._context import *
from ._template import *
import jinja2


class IRenderer(abc.ABC):
    @abc.abstractmethod
    def __init__(self, context: Optional[IContext] = None, template: Optional[ITemplate] = None, **kwargs):
        pass

    @property
    @abc.abstractmethod
    def context(self) -> Optional[IContext]:
        pass

    @context.setter
    @abc.abstractmethod
    def context(self, value: IContext):
        pass

    @property
    @abc.abstractmethod
    def template(self) -> Optional[ITemplate]:
        pass

    @template.setter
    @abc.abstractmethod
    def template(self, value: ITemplate):
        pass

    @abc.abstractmethod
    def render(self):
        pass

    @property
    @abc.abstractmethod
    def jinja_environment(self) -> jinja2.Environment:
        pass
