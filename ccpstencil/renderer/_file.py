__all__ = [
    'FileRenderer',
]

from ccpstencil.structs import *
from pathlib import Path
from ._string import *


class FileRenderer(StringRenderer):
    def __init__(self, output_file: Union[str, Path],
                 context: Optional[IContext] = None, template: Optional[ITemplate] = None,
                 overwrite: bool = True,
                 **kwargs):
        if isinstance(output_file, str):
            output_file = Path(output_file)
        self._output_file: Path = output_file
        self._overwrite = overwrite
        super().__init__(context, template, **kwargs)

    def render(self) -> str:
        return super().render()

    def _output_rendered_results(self, rendered_string: str) -> str:
        results = self._render_as_string()
        if results is None:
            return f'Skipped: {self._output_file.absolute()}'

        if self._output_file.exists() and not self._overwrite:
            raise OutputFileExistsError(f'The target output file already exists and overwriting is'
                                        f' disabled: {self._output_file.absolute()}')
        self._output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self._output_file, 'w') as fout:
            fout.write(results)
        return str(self._output_file.absolute())

