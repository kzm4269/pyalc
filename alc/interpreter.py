import argparse
import readline
import shlex

from .completer import Completer
from .display import display
from .parse import extract_titles
from .path import CACHE_ROOT
from .search import search

_CACHE_DIR = CACHE_ROOT / 'interpreter'


def _setup_readline(history_path, completer):
    readline.parse_and_bind(r'tab: complete')
    readline.parse_and_bind(r'set editing-mode emacs')
    readline.parse_and_bind(r'set completion-ignore-case on')
    readline.set_completer_delims(r'')
    readline.set_completer(completer)
    try:
        readline.read_history_file(history_path)
    except FileNotFoundError:
        readline.write_history_file(history_path)


def _argument_parser():
    parser = argparse.ArgumentParser(prog='')
    parser.add_argument(
        'query',
        type=str,
        nargs='*',
        help='search string',
    )
    parser.add_argument(
        '-n',
        type=int,
        default=5,
        help='number of results',
    )
    parser.add_argument(
        '--exit',
        default=False,
        const=True,
        action='store_const',
    )
    return parser


def run():
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    history_path = _CACHE_DIR / 'history.txt'
    completer = Completer(_CACHE_DIR / 'complete.sqlite3')

    _setup_readline(history_path, completer)
    parser = _argument_parser()

    while True:
        try:
            try:
                input_text = input('\x1b[36m>>> \x1b[0m')
            except KeyboardInterrupt:
                print()
                continue
            except EOFError:
                print()
                break

            try:
                args = parser.parse_args(shlex.split(input_text))
            except SystemExit:
                continue

            if args.exit:
                print()
                break

            if args.query:
                dom = search(' '.join(args.query))
                display(dom, n=args.n)
                completer.extend(reversed(list(extract_titles(dom))))
        finally:
            readline.write_history_file(history_path)
