import os
import sys
import click

from transcode.environment import Environment
from transcode.common import add_common_options

CONTEXT_SETTINGS = dict(
    auto_envvar_prefix='TRANSCODE',
    help_option_names=['-h', '--help']
)

pass_environment = click.make_pass_decorator(Environment, ensure=True)
cmd_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'commands')
)

class TranscodeCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('transcode.commands.' + name,
                             None, None, ['cli'])
        except ImportError:
            return
        return mod.cli


@click.command(cls=TranscodeCLI, context_settings=CONTEXT_SETTINGS)
@add_common_options
@pass_environment
def cli(ctx):
    stdin = click.get_text_stream('stdin')

    if not stdin.isatty():
        ctx.subjects.append(''.join(stdin.readlines()))
