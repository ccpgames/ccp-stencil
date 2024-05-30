__all__ = [
    'DirectoryRenderer',
]

from ccpstencil.structs import *
from pathlib import Path

from . import FileRenderer
from ._base import *
from ccpstencil.template import DirectoryTemplate
import shutil
import logging

from ..template import FileTemplate

log = logging.getLogger(__file__)


class DirectoryRenderer(_BaseRenderer):
    _VALID_TEMPLATES = (DirectoryTemplate,)

    def __init__(self, output_path: T_PATH,
                 context: Optional[IContext] = None,
                 template: Optional[DirectoryTemplate] = None,
                 overwrite: bool = True,
                 purge: bool = True,
                 **kwargs):
        self._overwrite = overwrite
        self._purge = purge
        self._output_path = output_path
        self._rendered: List[str] = []
        if isinstance(self._output_path, str):
            self._output_path = Path(self._output_path)
        super().__init__(context, template, **kwargs)

    def _ensure_root(self):
        self._do_purge()
        if not self._output_path.exists():
            log.debug(f'Creating target output root path: {self._output_path}...')
            self._output_path.mkdir(parents=True, exist_ok=True)

    def _do_purge(self):
        if self._purge:
            if self._output_path.exists():
                if not self._overwrite:
                    raise OutputFileExistsError(f'Purge is enabled but the target output path already exists and overwriting is disabled: {self._output_path}')
                log.debug(f'Purging output path: {self._output_path}...')
                shutil.rmtree(self._output_path.absolute(), ignore_errors=True)

    def _make_dir(self, dir_template: DirectoryTemplate) -> bool:
        full_path = self._output_path / dir_template.target_path
        if dir_template.skip_me:
            log.debug(f'Skipping due to skip_if tag: {full_path}...')
            return False
        else:
            log.debug(f'Creating relative directory: {full_path}...')
            full_path.mkdir(exist_ok=True)
            return True

    def _build_tree(self):
        def _build_tree_inner(dir_template: DirectoryTemplate):
            for dt in dir_template.directories:
                if self._make_dir(dt):
                    _build_tree_inner(dt)
        _build_tree_inner(self.template)  # noqa

    def _render_file(self, template: FileTemplate, target_path: Optional[Path] = None):
        log.debug(f'Rendering {template}...')
        if target_path:
            p = self._output_path / target_path / template.file_name
        else:
            p = self._output_path / template.file_name
        r = FileRenderer(output_path=p,
                         context=self.context,
                         template=template,
                         overwrite=self._overwrite)
        res = r.render()
        if target_path:
            rp = target_path / template.file_name
        else:
            rp = template.file_name
        if res is None:
            log.debug(f'Skipped rendering {rp} due to skip_if tag...')
        else:
            log.debug(f'Rendered: {rp}')
            self._rendered.append(str(p))

    def _build_files(self):
        def _build_files_inner(dir_template: DirectoryTemplate):
            if dir_template.skip_me:
                return
            for f in dir_template.files:
                self._render_file(f, None if dir_template.is_root else dir_template.target_path)
            for dt in dir_template.directories:
                _build_files_inner(dt)

        _build_files_inner(self.template)  # noqa

    def render(self) -> List[str]:
        self._pre_flight()
        self._ensure_root()
        self._build_tree()
        self._build_files()
        return self._rendered

    def _output_rendered_results(self, rendered_string: str) -> str:
        pass

    def _render_as_string(self) -> str:
        pass

    @property
    def output_file_name(self) -> Optional[str]:
        pass

    @output_file_name.setter
    def output_file_name(self, value: str):
        pass

