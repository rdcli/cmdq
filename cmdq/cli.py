from argparse import ArgumentParser
import sys
from os import system

from .queue import CommandQueue
from .resource import ResourcePool
from .env import getenv

def log_decorator(function):
    def wrapper(*args, **kwargs):
        print '>>> %s %r %r' % (function.__name__, args, kwargs, )
        return function(*args, **kwargs)
    wrapper.__name__ = function.__name__
    return wrapper

def generate_script(config, thread_count):
    """Generate a closure that can run multithreaded script.

    """

    # Prepare initializable stuff.
    initializable_commands = [config_bit.initialize for name, config_bit in
            config.iteritems() if isinstance(config_bit, ResourcePool)]
    initializable_commands_count = len(initializable_commands)

    # Prepare finalizable stuff.
    finalizable_commands = [config_bit.finalize for name, config_bit in
            config.iteritems() if isinstance(config_bit, ResourcePool)]
    finalizable_commands_count = len(finalizable_commands)

    def script():
        # Actual initialization.
        if initializable_commands_count:
            print '>>> Initialize resources (%d steps)' % (initializable_commands_count, )
            CommandQueue(commands=initializable_commands, thread_count=thread_count).run()

        # Actual command queue.
        CommandQueue(commands=config['cmdq'], thread_count=thread_count).run()

        # Actual finalization.
        if finalizable_commands_count:
            print '>>> finalize resources (%d steps)' % (finalizable_commands_count, )
            CommandQueue(commands=finalizable_commands, thread_count=thread_count).run()

    return script

def load_configuration(filename):
    """Loads cmdq configuration file and make sanity checks.

    """

    with open(filename) as f:
        code = compile(f.read(), filename, 'exec')

    config = {
        'getenv': getenv,
        'ResourcePool': ResourcePool,
        'system': log_decorator(system),
    }

    try:
        exec code in config
    except Exception, e:
        print 'A %s happened while parsing your configuration file.' % (e.__class__.__name__, )
        print 'Message: %s' % (e.message, )
        print
        raise
        sys.exit(1)

    if not 'cmdq' in config:
        raise Exception, 'Please provide a cmdq local in your config file.'

    return config

def main():
    """Console script entry point"""

    parser = ArgumentParser('cmdq')
    parser.add_argument('filename', help='Config filename.')
    parser.add_argument('--thread-count', type=int, default=4, help='Thread count.')
    args = parser.parse_args()

    config = load_configuration(args.filename)
    script = generate_script(config, args.thread_count)
    script()

