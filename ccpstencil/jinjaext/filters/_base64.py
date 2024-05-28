__all__ = [
    'base64',
]

import base64 as _base64


def base64(value: str) -> str:
    return _base64.encodebytes(value.encode('utf-8')).decode('utf-8').strip()
