from argparse import ArgumentParser
import sys
from os import system

from .queue import CommandQueue
from .resource import ResourcePool

def log_decorator(function):
    def wrapper(*args, **kwargs):
        print '>>> %s %r %r' % (function.__name__, args, kwargs, )
        return function(*args, **kwargs)
    wrapper.__name__ = function.__name__
    return wrapper

def main():
    """Console script entry point"""

    parser = ArgumentParser('cmdq')
    parser.add_argument('filename', help='Config filename.')
    parser.add_argument('--thread-count', type=int, default=4, help='Thread count.')
    args = parser.parse_args()

    with open(args.filename) as f:
        code = compile(f.read(), args.filename, 'exec')

    config = {
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

    CommandQueue(commands=config['cmdq'], thread_count=args.thread_count).run()

    for name, config_bit in config.iteritems():
        if isinstance(config_bit, ResourcePool):
            config_bit.finalize()

