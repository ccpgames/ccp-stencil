__all__ = [
    'SkipIfExtension',
]
from jinja2 import nodes
from jinja2.ext import Extension
from ccpstencil.structs import *


class SkipIfExtension(Extension):
    tags = {'skip_if'}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        # Parse the condition expression
        condition = parser.parse_expression()
        return nodes.CallBlock(self.call_method('_check_condition', [condition]), [], [], []).set_lineno(lineno)

    def _check_condition(self, condition, caller):
        if condition:
            raise CancelRendering("Rendering cancelled due to meta_only_render_if condition being False")
        return ''
