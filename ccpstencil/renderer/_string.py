__all__ = [
    'StringRenderer',
]

from ccpstencil.structs import *
from ._base import *


class StringRenderer(_BaseRenderer):
    def __init__(self, context: Optional[IContext] = None, template: Optional[ITemplate] = None, **kwargs):
        super().__init__(context, template, **kwargs)

    def render(self) -> Optional[str]:
        return super().render()

    def _render_as_string(self) -> str:
        return self.template.get_jinja_template().render(**self.context.as_dict())

    def _output_rendered_results(self, rendered_string: str) -> str:
        return rendered_string
