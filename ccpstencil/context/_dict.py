__all__ = [
    'DictContext',
]

from ccpstencil.structs import *
from ccptools.tpu import iters
import logging
log = logging.getLogger(__file__)


class DictContext(IContext):
    def __init__(self, context_map: Dict[str, Any] = None, **kwargs):
        self._context_map = context_map or {}

    def update(self, key: str, value: Any):
        self._context_map[key] = value

    def nested_update(self, key_tuple: Union[str, Tuple[str]], value: Any):
        log.debug(f'nested_update({key_tuple=}, {value=})')
        if isinstance(key_tuple, str):
            key_tuple = key_tuple.split('.')
        if isinstance(key_tuple, List):
            key_tuple = tuple(key_tuple)
        iters.nested_set(self._context_map, key_tuple, value)

    def as_dict(self) -> Dict:
        return self._context_map
