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
        return state.reverse

    return click.option(
        '-r', '--reverse', is_flag=True,
        expose_value=False,
        default=None,   # Disable click default mechanism
        help='ie. transcode hex -r 0xDEADBEEF',
        callback=callback
    )(f)


def add_unsafe_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(Environment)
        if value is not None:
            state.unsafe = value
        return state.unsafe

    return click.option(
        '-u', '--unsafe', is_flag=True,
        default=None,   # Disable click default mechanism
        expose_value=False,
        help='Prints raw output, can damage TTY !',
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
        metavar='<str>',
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
        metavar='<str>',
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
        metavar='<str>',
        callback=callback
    )(f)


def add_common_options(f):
    f = add_verbosity_option(f)
    f = add_reverse_option(f)
    f = add_unsafe_option(f)
    f = add_prefix_option(f)
    f = add_suffix_option(f)
    f = add_separator_option(f)

    return f
