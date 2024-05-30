__all__ = [
    'FileTemplate',
]

from ccpstencil.structs import *
from pathlib import Path

from ._base import *


class FileTemplate(_BaseTemplate):
    def __init__(self, file_path: T_PATH, **kwargs):
        super().__init__(**kwargs)
        self._file_path: T_PATH = file_path

    def _read_file(self) -> str:
        as_path = self.get_file_path()

        if not as_path.exists():
            raise TemplateNotFoundError(f'File {as_path} does not exist')

        with open(as_path, 'r') as fin:
            return fin.read()

    def get_file_path(self) -> Path:
        if isinstance(self._file_path, str):
            return Path(self._file_path)
        return self._file_path

    def get_jinja_template(self) -> jinja2.Template:
        if isinstance(self._file_path, str):
            try:
                return self.renderer.jinja_environment.get_template(self._file_path)
            except jinja2.exceptions.TemplateNotFound:
                pass
        template_string = self._read_file()
        return self.renderer.jinja_environment.from_string(template_string)
