__all__ = [
    'DirectoryTemplate',
]

import logging

from ccpstencil.structs import *
from pathlib import Path

from ._base import *
from ._file import *

import logging
log = logging.getLogger(__file__)


class DirectoryTemplate(_BaseTemplate):
    def __init__(self, dir_path: T_PATH, parent: Optional['DirectoryTemplate'] = None, **kwargs):
        super().__init__(**kwargs)
        if isinstance(dir_path, str):
            dir_path = Path(dir_path)
        self._dir_path: Path = dir_path

        if not self._dir_path.exists():
            raise TemplateNotFoundError(f'Template root does not exist: {self._dir_path}')

        if not self._dir_path.is_dir():
            raise TemplateNotFoundError(f'Template root is not a directory: {self._dir_path}')

        self._directories: List[DirectoryTemplate] = []
        self._files: List[FileTemplate] = []
        self._meta_file: Optional[Path] = None

        self._parent = parent

        self._target_name: Optional[str] = None
        self._skip_me: bool = False
        self._is_rendered: bool = False

        self._crawl()

    @property
    def is_root(self) -> bool:
        return self._parent is None

    @property
    def absolute_source_path(self) -> Path:
        """This is the full absolute path to the source template directory!"""
        if self.is_root:
            return self._dir_path.absolute()
        return self._parent.absolute_source_path / self.source_name

    @property
    def source_path(self) -> Path:
        """This is the relative path to the source template directory!"""
        if self.is_root:
            return Path('.')
        return self._parent.source_path / self.source_name

    @property
    def source_name(self) -> str:
        """This is name of the source template directory!"""
        return self._dir_path.name

    @property
    def target_path(self) -> Path:
        """This is the relative path to the rendered target path"""
        if self.is_root:
            return Path('.')
        return self._parent.target_path / self.target_name

    @property
    def target_name(self) -> str:
        """This is name of the target directory to render (can be different from source name via __stencil_meta__)"""
        self._render_target_name()
        return self._target_name

    @property
    def skip_me(self) -> bool:
        self._render_target_name()
        return self._skip_me

    def _render_target_name(self):
        if not self._is_rendered:
            self._is_rendered = True
            self._skip_me = False
            if self.meta_template:
                from ccpstencil.renderer import StringRenderer
                r = StringRenderer(context=self.renderer.context,
                                   template=self.meta_template)
                result = r.render()
                if r.output_file_name != '__stencil_meta__':
                    self._target_name = r.output_file_name
                else:
                    self._target_name = self.source_name

                if result is None:
                    self._skip_me = True
            else:
                self._target_name = self.source_name

    def set_renderer(self, renderer: IRenderer):
        super().set_renderer(renderer)
        for d in self._directories:
            d.set_renderer(renderer)

    @property
    def meta_template(self) -> Optional[FileTemplate]:
        if self._meta_file:
            return FileTemplate(file_path=self._meta_file.absolute())
        return None

    @property
    def directories(self) -> List['DirectoryTemplate']:
        return self._directories

    @property
    def files(self) -> List['FileTemplate']:
        return self._files

    def _crawl(self):
        for i in self._dir_path.iterdir():
            if i.is_dir():
                self._directories.append(DirectoryTemplate(i, parent=self))
            else:
                if i.name == '__stencil_meta__':
                    self._meta_file = i
                    if self._parent is None:
                        raise TemplateError('The __stencil_meta__ file is not allowed in the template root directory')
                else:
                    log.debug(f'Adding {self.absolute_source_path} / {i.name}')
                    self._files.append(FileTemplate(self.absolute_source_path / i.name))

    def dump_lines(self) -> List[str]:
        s = []
        if self._parent is None:
            s.append('I AM ROOT:')

        for d in self._directories:
            s.append(f'+- {d.source_name}/ [{d.target_path}]')
            for x in d.dump_lines():
                s.append(f'|     {x}')
        for f in self._files:
            s.append(f'+- {f.file_name} [{f.get_file_path()}]')
        return s

    def dump(self) -> str:
        return '\n'.join(self.dump_lines())

    def get_jinja_template(self) -> jinja2.Template:
        pass


