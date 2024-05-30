__all__ = [
    'FileRenderer',
]

from ccpstencil.structs import *
from pathlib import Path
from ._string import *


class FileRenderer(StringRenderer):
    def __init__(self, output_path: Union[str, Path],
                 context: Optional[IContext] = None, template: Optional[ITemplate] = None,
                 overwrite: bool = True,
                 **kwargs):
        if isinstance(output_path, str):
            output_path = Path(output_path)
        self._output_path: Path = output_path
        if not self._output_path.is_dir():
            self.output_file_name = self._output_path.name
            self._output_path = self._output_path.parent

        self._overwrite = overwrite
        super().__init__(context, template, **kwargs)

    def render(self) -> str:
        return super().render()

    def _output_rendered_results(self, rendered_string: str) -> str:
        results = self._render_as_string()
        fout_path = self.output_file()
        if results is None:
            return f'Skipped: {fout_path.absolute()}'

        if fout_path.exists() and not self._overwrite:
            raise OutputFileExistsError(f'The target output file already exists and overwriting is'
                                        f' disabled: {fout_path.absolute()}')
        fout_path.parent.mkdir(parents=True, exist_ok=True)

        with open(fout_path, 'w') as fout:
            fout.write(results)
        return str(fout_path.absolute())

    def output_file(self) -> Path:
        name = self.output_file_name
        if name is None:
            raise NoOutputFileNameError('no output file name set or found')
        return self._output_path / Path(self.output_file_name)

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
        self._output_file_name = value