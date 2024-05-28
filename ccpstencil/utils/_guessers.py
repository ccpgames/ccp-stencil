__all__ = [
    'guess_template_by_argument',
    'guess_context_by_argument',
]

from ccpstencil.context import *
from ccpstencil.template import *
from ccpstencil.structs import *

from pathlib import Path


def guess_template_by_argument(template: T_PATH, renderer: Optional[IRenderer] = None) -> ITemplate:
    if isinstance(template, Path):
        return FileTemplate(file_path=template)

    if len(template.splitlines()) > 1:
        return StringTemplate(template_string=template)

    if renderer and isinstance(template, str):
        if renderer.is_template_loadable(template):
            return FileTemplate(file_path=template)
    as_path = Path(template)
    if as_path.exists():
        return FileTemplate(file_path=template)
    return StringTemplate(template_string=template)


def guess_context_by_argument(context: Union[str, Path, Dict]) -> IContext:
    if isinstance(context, Path):
        return AlvissContext(file_name=context)
    if isinstance(context, Dict):
        return DictContext(context_map=context)
    return AlvissContext(file_name=context)
