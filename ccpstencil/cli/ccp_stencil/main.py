import argparse

from ccpstencil import __version__ as version
from ccpstencil.structs import *
from ._runner import StencilRunner

import sys


def main():
    parser = argparse.ArgumentParser(description='Renders a template using Jinja2 and Alviss input context',
                                     epilog=f'CCP-Stencil version {version}')

    parser.add_argument('-v', '--verbose', action="store_true", help='Spits out DEBUG level logs')

    parser.add_argument('-i', '--input', nargs='?', help='Alviss file with input context (YAML or JSON)')

    parser.add_argument('-a', '--arg', action='append', help='Add additional Context arguments from the command line, e.g. -a foo=bar')

    parser.add_argument('-o', '--output', help='Path or file to write the results to (otherwise its just printed to stdout).'
                                               ' If this is a path (ends with /), the name of the rendered file will be the same as the input template.',
                              default='', nargs='?')
    parser.add_argument('--no-overwrite', action="store_true", help='Makes sore existing output files are not overwritten')
    parser.add_argument('--no-purge', action="store_true", help='Skips purging the output path when rendering directories')

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-t', '--template', default='',
                             help='Template file to render')
    input_group.add_argument('-s', '--string-template', default='',
                             help='Supply a string directly from the command line to use as a template instead of a file')
    input_group.add_argument('-d', '--directory-template', default='',
                             help='Root directory of files and directories to render. This requires the output argument to be a directory')

    args = parser.parse_args()

    if args.verbose:
        import logging
        logging.basicConfig(level=logging.DEBUG)

        log = logging.getLogger(__name__)
        log.info('Verbose logging enabled')
        log.info(f'Args: {args=}')

    runner = StencilRunner()
    runner.verbose = args.verbose or False
    runner.input = args.input or None
    runner.output = args.output or None
    runner.no_overwrite = args.no_overwrite or False
    runner.no_purge = args.no_purge or False
    runner.template = args.template or None
    runner.string_template = args.string_template or None
    runner.directory_template = args.directory_template or None
    if args.arg:
        for arg in args.arg:
            runner.additional_arg_list.append(arg)

    try:
        runner.run()
    except StencilError as e:
        print(f'An error occurred: {e!r}', file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
