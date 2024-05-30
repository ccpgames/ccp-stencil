__all__ = [
    'SetFilenameExtension',
]

from jinja2 import nodes
from jinja2.ext import Extension
from ccpstencil.structs import *


class SetFilenameExtension(Extension):
    tags = {'setfilename'}

    def __init__(self, environment):
        super().__init__(environment)
        environment.extend(stencil_renderer=None)

    @property
    def renderer(self) -> IRenderer:
        return self.environment.stencil_renderer  # noqa

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        body = parser.parse_statements(('name:endsetfilename',), drop_needle=True)
        return nodes.CallBlock(self.call_method('_set_filename', []), [], [], body).set_lineno(lineno)

    def _set_filename(self, caller):
        self.renderer.output_file_name = caller().strip()
        return ''
