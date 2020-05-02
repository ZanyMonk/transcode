import re
import sys
import click
from typing import Pattern, Callable
from colorama import Fore, Back, Style


class Environment(object):
    def __init__(self):
        self.verbosity = 0
        self.reverse = False
        self.unsafe = False
        self._prefix = None
        self._suffix = None
        self._separator = None
        self.subjects = []

    @property
    def decode_mode(self):
        return 'replace' if self.unsafe else 'backslashreplace'

    @property
    def has_prefix(self):
        return self._prefix is not None

    @property
    def prefix(self):
        return self._prefix if self.has_prefix else ''

    @prefix.setter
    def prefix(self, prefix):
        self._prefix = prefix

    @property
    def suffix(self):
        return self._suffix if self._suffix is not None else ''

    @property
    def has_suffix(self):
        return self._suffix is not None

    @suffix.setter
    def suffix(self, suffix):
        self._suffix = suffix

    @property
    def separator(self):
        return self._separator if self._separator is not None else ''

    @property
    def has_separator(self):
        return self._separator is not None

    @separator.setter
    def separator(self, separator):
        self._separator = separator

    def gen_trans_table(self, subject: str, pattern: Pattern, transform: Callable):
        return{m: transform(m) for m in set(re.findall(pattern, subject))}

    def translate(self, subject: str, table: dict):
        return ''.join([table[c] if c in table else c for c in subject])

    def split(self, subject):
        return re.split(self._separator, subject)

    def strip_fixes(self, subject):
        if self._prefix is not None:
            m = re.search(self._prefix, subject)
            if m is not None:
                subject = subject[m.end():]

        if self._suffix is not None:
            m = re.search(self._suffix, subject)
            if m is not None:
                subject = subject[:m.start()]

        return subject

    def output(self, data):
        if self.unsafe:
            click.get_binary_stream('stdout').write(data)
        else:
            print(data.decode('utf-8', self.decode_mode))

    def log(self, msg, output=sys.stdout, *args):
        """Logs a message to stderr."""
        click.echo(msg, file=output, *args)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbosity is enabled."""
        if self.verbosity:
            self.log(msg, *args)

    def elog(self, msg, *args):
        """Logs a message to stderr only if verbosity is enabled."""
        self.log('{}[FAILED]{} {}'.format(Fore.RED, Fore.RESET, msg), sys.stderr, *args)
