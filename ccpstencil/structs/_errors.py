__all__ = [
    'StencilError',

    'TemplateError',
    'TemplateNotFoundError',

    'ContextError',

    'RenderError',
    'NoTemplateSetError',
    'InvalidContextTypeForRendererError',
    'InvalidTemplateTypeForRendererError',
    'OutputFileExistsError',
    'EmbedFileNotFound',

    'CancelRendering',
]


class StencilError(Exception):
    pass


class TemplateError(StencilError):
    pass


class TemplateNotFoundError(TemplateError, FileNotFoundError):
    pass


class ContextError(StencilError):
    pass


class RenderError(StencilError):
    pass


class NoTemplateSetError(RenderError, ValueError):
    pass


class InvalidContextTypeForRendererError(RenderError, TypeError):
    pass


class InvalidTemplateTypeForRendererError(RenderError, TypeError):
    pass


class OutputFileExistsError(RenderError, FileExistsError):
    pass


class EmbedFileNotFound(RenderError, FileNotFoundError):
    pass


class CancelRendering(Exception):
    pass
