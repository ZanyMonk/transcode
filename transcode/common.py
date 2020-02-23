import click
from transcode.environment import Environment

def add_verbosity_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(Environment)
        if value is not None:
            state.verbosity = value
            return value

    return click.option(
        '-v', '--verbosity', count=True,
        default=None,
        expose_value=False,
        help='Set verbosity level.',
        callback=callback
    )(f)

def add_reverse_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(Environment)
        if value is not None:
            state.reverse = value
            return value
        return state.reverse

    return click.option(
        '-r', '--reverse', is_flag=True,
        expose_value=False,
        help='ie. transcode hex -r 0xDEADBEEF',
        callback=callback
    )(f)

def add_prefix_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(Environment)
        if value is not None:
            state.prefix = value
            return value

    return click.option(
        '-P', '--prefix', default=None,
        expose_value=False,
        help='String added in front of the output.',
        callback=callback
    )(f)

def add_suffix_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(Environment)
        if value is not None:
            state.suffix = value
            return value

    return click.option(
        '-S', '--suffix', default=None,
        expose_value=False,
        help='String added at the end of the output.',
        callback=callback
    )(f)

def add_separator_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(Environment)
        if value is not None:
            state.separator = value
            return value

    return click.option(
        '-s', '--separator', default=None,
        expose_value=False,
        help='String added in between each char.',
        callback=callback
    )(f)

def add_common_options(f):
    f = add_verbosity_option(f)
    f = add_reverse_option(f)
    f = add_prefix_option(f)
    f = add_suffix_option(f)
    f = add_separator_option(f)

    return f