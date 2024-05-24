__all__ = [
    'IContext',
]
from ccptools.structs import *


class IContext(abc.ABC):
    @abc.abstractmethod
    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def update(self, key: str, value: Any):
        pass

    @abc.abstractmethod
    def nested_update(self, key_tuple: Union[str, Tuple[str]], value: Any):
        pass

    @abc.abstractmethod
    def as_dict(self) -> Dict:
        pass
