__all__ = [
    'EmbedExtension',
]

from jinja2 import nodes
from jinja2.ext import Extension
from ccpstencil.structs import *


class EmbedExtension(Extension):
    tags = {'embed'}

    def __init__(self, environment):
        super().__init__(environment)
        environment.extend(stencil_renderer=None)

    @property
    def renderer(self) -> IRenderer:
        return self.environment.stencil_renderer  # noqa

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        source_file = parser.filename
        kwargs = [nodes.Keyword('source_file', nodes.Const(source_file))]
        while parser.stream.skip_if('comma'):
            key = parser.stream.expect('name').value
            parser.stream.expect('assign')
            value = parser.parse_expression()
            kwargs.append(nodes.Keyword(key, value))

        return nodes.CallBlock(self.call_method('_render_embed', args, kwargs), [], [], []).set_lineno(lineno)

    def _render_embed(self, file_path, source_file: Optional[str] = None, indent: int = 0,
                      alviss: bool = False, env: bool = False,  caller=None, **kwargs):

        # Check if file_path is a variable in the context
        if hasattr(file_path, '__call__'):
            file_path = file_path()

        content = self.renderer.get_embed(file_path, alviss=alviss, env=env)

        # Detect the current line's indentation level
        if indent:
            indent_str = ' '*indent
        else:
            indent_str = ''

        joiner = f'{indent_str}'

        return f'{indent_str}{joiner.join(content.splitlines(True))}\n'
