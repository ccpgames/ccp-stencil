__all__ = [
    '_BaseRenderer',
]

import os
import sys
from pathlib import Path
from ccptools.tpu import strimp
from ccpstencil.structs import *
from jinja2.ext import Extension
from alviss import quickloader

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
        self._search_paths: List[Path] = []
        self._load_search_paths()
        self._env: jinja2.Environment = self._make_environment()
        self._load_filters()
        self._output_file_name: Optional[str] = None

    def _make_environment(self) -> jinja2.Environment:
        env = jinja2.Environment(
            lstrip_blocks=True,
            trim_blocks=True,
            keep_trailing_newline=True,
            undefined=jinja2.ChainableUndefined,
            extensions=self._get_extensions(),
            loader=jinja2.FileSystemLoader([str(p) for p in self._search_paths])
        )
        env.stencil_renderer = self
        return env

    def _get_extensions(self) -> List[Type[Extension]]:
        buffer_list = []
        extension_module = strimp.get_module('ccpstencil.jinjaext.extensions')
        for name, item in extension_module.__dict__.items():
            if name.startswith('_'):
                continue
            if issubclass(item, Extension):
                buffer_list.append(item)
        return buffer_list

    def _load_filters(self):
        filter_module = strimp.get_module('ccpstencil.jinjaext.filters')
        for name, item in filter_module.__dict__.items():
            if name.startswith('_'):
                continue
            if isinstance(item, Callable):
                self.jinja_environment.filters[name] = item

    def _load_search_paths(self):
        self._search_paths.append(Path(os.getcwd()).absolute())  # Current Working Directory!
        script_path = Path(sys.argv[0]).parent.absolute()
        if script_path not in self._search_paths:
            self._search_paths.append(script_path)
        stp = os.environ.get('STENCIL_TEMPLATE_PATH', None)  # Extra paths! :D
        if stp:
            for tp in stp.split(';'):
                tpp = Path(tp).absolute()
                if tpp not in self._search_paths:
                    self._search_paths.append(tpp)

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

    def render(self):
        self._pre_flight()
        try:
            rendered_string = self._render_as_string()
            return self._output_rendered_results(rendered_string)
        except CancelRendering:
            log.info(f'Rendering cancelled by skip_if tag')
            return None

    @abc.abstractmethod
    def _output_rendered_results(self, rendered_string: str):
        pass

    @abc.abstractmethod
    def _render_as_string(self) -> str:
        pass

    @property
    def jinja_environment(self) -> jinja2.Environment:
        return self._env

    def is_template_loadable(self, template_name: str) -> bool:
        try:
            self.jinja_environment.get_template(template_name)
            return True
        except jinja2.TemplateNotFound:
            return False

    def get_embed(self, file_path: str, source_file: Optional[str] = None,
                  alviss: bool = False, env: bool = False, fidelius: bool = False) -> str:
        as_path = Path(file_path)
        if as_path.is_absolute():
            if not as_path.exists():
                raise EmbedFileNotFound(f'Embed file not found via absolute path: {file_path}')
            return self._get_embed(file_path, alviss=alviss, env=env, fidelius=fidelius)

        search_paths = []

        if source_file:
            search_paths.append(Path(source_file).absolute().parent)

        search_paths += self._search_paths

        for p in search_paths:
            f = p / file_path
            if f.exists():
                return self._get_embed(str(f.absolute()), alviss=alviss, env=env, fidelius=fidelius)

        raise EmbedFileNotFound(f'Embed file not found in any search path: {file_path}')

    def _get_embed(self, abs_file_path: str, alviss: bool = False, env: bool = False, fidelius: bool = False) -> str:
        if alviss:
            return quickloader.render_load(abs_file_path,
                                           skip_env_loading=not env,
                                           skip_fidelius=not fidelius)

        else:
            with open(abs_file_path, 'r', newline=None) as fin:
                return fin.read()

    @property
    def output_file_name(self) -> Optional[str]:
        if self._output_file_name:
            return self._output_file_name

        if self._template:
            from ccpstencil.template import FileTemplate
            if isinstance(self._template, FileTemplate):
                return self._template.get_file_path().name

        return None

    @output_file_name.setter
    def output_file_name(self, value: str):
        self._output_file_name = value or None
