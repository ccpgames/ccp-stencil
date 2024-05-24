__all__ = [
    '_BaseRenderer',
]

from ccpstencil.structs import *

import jinja2

import logging
log = logging.getLogger(__file__)


class _BaseRenderer(IRenderer, abc.ABC):
    _VALID_CONTEXTS: Optional[Tuple[Type[IContext]]] = None
    _INVALID_CONTEXTS: Optional[Tuple[Type[IContext]]] = None

    _VALID_TEMPLATES: Optional[Tuple[Type[ITemplate]]] = None
    _INVALID_TEMPLATES: Optional[Tuple[Type[ITemplate]]] = None

    def __init__(self, context: Optional[IContext] = None, template: Optional[ITemplate] = None, **kwargs):
        self._context = None
        self._template = None
        # This is to trigger the Setters!
        if context is not None:
            self.context = context
        if template is not None:
            self.template = template
        if kwargs:
            log.warning(f'Unrecognized kwargs for {self.__class__.__name__}: {kwargs}')
        self._env: jinja2.Environment = self._make_environment()

    def _make_environment(self) -> jinja2.Environment:
        return jinja2.Environment(
            lstrip_blocks=True,
            trim_blocks=True,
            undefined=jinja2.ChainableUndefined
        )

    def _pre_flight(self):
        if not self.template:
            raise NoTemplateSetError(f'No template set for {self.__class__.__name__}')

    def _is_valid_context(self, context: IContext) -> bool:
        if self._INVALID_CONTEXTS:  # Deny?
            if isinstance(context, self._INVALID_CONTEXTS):
                return False

        if self._VALID_CONTEXTS:  # Allow?
            if isinstance(context, self._VALID_CONTEXTS):
                return True
            return False  # If there is an "allow list" then we deny everything else!
        return True

    def _is_valid_template(self, template: ITemplate) -> bool:
        if self._INVALID_TEMPLATES:  # Deny?
            if isinstance(template, self._INVALID_TEMPLATES):
                return False

        if self._VALID_TEMPLATES:  # Allow?
            if isinstance(template, self._VALID_TEMPLATES):
                return True
            return False  # If there is an "allow list" then we deny everything else!
        return True

    @property
    def context(self) -> Optional[IContext]:
        return self._context

    @context.setter
    def context(self, value: IContext):
        if not self._is_valid_context(value):
            raise InvalidContextTypeForRendererError(f'Context of {value.__class__.__name__} type does not work with a {self.__class__.__name__} Renderer')
        self._context = value

    @property
    def template(self) -> Optional[ITemplate]:
        return self._template

    @template.setter
    def template(self, value: ITemplate):
        if not self._is_valid_template(value):
            raise InvalidTemplateTypeForRendererError(f'Template of {value.__class__.__name__} type does not work with a {self.__class__.__name__} Renderer')
        value.set_renderer(self)
        self._template = value

    @abc.abstractmethod
    def render(self):
        """This should just be called by subclasses via super().render() in
        order to run preflight and common stuff, but the empty return value
        should be ignored.
        """
        self._pre_flight()

    @property
    def jinja_environment(self) -> jinja2.Environment:
        return self._env

