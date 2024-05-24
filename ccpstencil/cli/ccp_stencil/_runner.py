__all__ = [
    'StencilRunner',
]
from ccptools.structs import *
from ccpstencil.stencils import *
import logging
log = logging.getLogger(__file__)


class StencilRunner:
    def __init__(self):
        self.verbose: bool = False

        self.template: Optional[str] = None
        self.string_template: Optional[str] = None

        self.input: Optional[str] = None
        self.additional_arg_list: List[str] = []

        self.output: Optional[str] = None
        self.no_overwrite: bool = False

    def run(self):
        rnd = self.get_renderer()
        rnd.template = self.get_template()
        rnd.context = self.get_context()
        rnd.render()

    def get_template(self) -> ITemplate:
        if self.template:
            return FileTemplate(self.template)
        else:
            return StringTemplate(self.string_template)

    def _parse_arg(self, arg_str: str) -> Tuple[str, str]:
        log.debug(f'_parse_arg({arg_str})')
        return tuple(arg_str.split('=', maxsplit=1))  # noqa

    def get_context(self) -> IContext:
        if self.input:
            ctx = AlvissContext(self.input)
        else:
            ctx = DictContext()

        if self.additional_arg_list:
            for arg in self.additional_arg_list:
                ctx.nested_update(*self._parse_arg(arg))
        return ctx

    def get_renderer(self) -> IRenderer:
        if self.output:
            return FileRenderer(self.output,
                                overwrite=not self.no_overwrite)
        else:
            return StdOutRenderer()
