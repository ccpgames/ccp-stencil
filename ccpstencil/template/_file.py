__all__ = [
    'FileTemplate',
]

from ccpstencil.structs import *
from pathlib import Path

from ._string import *


class FileTemplate(StringTemplate):
    def __init__(self, file_path: Union[str, Path], **kwargs):
        if isinstance(file_path, str):
            file_path = Path(file_path)
        self._file_path: Path = file_path
        super().__init__(template_string=self._read_file(), **kwargs)

    def _read_file(self) -> str:
        if not self._file_path.exists():
            raise TemplateNotFoundError(f'File {self._file_path} does not exist')

        with open(self._file_path, 'r') as fin:
            return fin.read()
