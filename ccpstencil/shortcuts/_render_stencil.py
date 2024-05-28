__all__ = [
    'render_stencil',
]


from ccpstencil.stencils import *
from ccpstencil.utils import *
from ccpstencil.structs import *


def render_stencil(template: T_PATH, context: Union[Dict, T_PATH]) -> str:
    renderer = StringRenderer()
    template = guess_template_by_argument(template, renderer)
    context = guess_context_by_argument(context)
    renderer.template = template
    renderer.context = context
    return renderer.render()
