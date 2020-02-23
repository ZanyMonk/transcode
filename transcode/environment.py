import re

class Environment(object):
	def __init__(self):
		self.verbosity = 0
		self.reverse = False
		self.prefix = None
		self.suffix = None
		self.separator = None
		self.subjects = []

	def get_prefix(self):
		return self.prefix if self.prefix is not None else ''

	def get_suffix(self):
		return self.suffix if self.suffix is not None else ''

	def get_separator(self):
		return self.separator if self.separator is not None else ''

	def split(self, subject):
		return re.split(self.separator, subject)

	def strip_fixes(self, subject):
		if self.prefix is not None:
			m = re.search(self.prefix, subject)
			if m is not None:
				subject = subject[m.end():]

		if self.suffix is not None:
			m = re.search(self.suffix, subject)
			if m is not None:
				subject = subject[:m.start()]

		return subject

	def log(self, msg, *args):
		"""Logs a message to stderr."""
		if args:
			msg %= args
		click.echo(msg, file=sys.stderr)

	def vlog(self, msg, *args):
		"""Logs a message to stderr only if verbosity is enabled."""
		if self.verbosity:
			self.log(msg, *args)
