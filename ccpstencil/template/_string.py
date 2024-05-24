__all__ = [
    'StringTemplate',
]

import jinja2

from ._base import *


class StringTemplate(_BaseTemplate):
    def __init__(self, template_string: str, **kwargs):
        super().__init__(**kwargs)
        self._template_string = template_string

    def get_jinja_template(self) -> jinja2.Template:
        return self.renderer.jinja_environment.from_string(self._template_string)
