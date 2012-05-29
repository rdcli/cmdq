from argparse import ArgumentParser
from threading import Thread
from time import sleep

class CommandQueue(object):
    """Class to configure a command queue, that will run `commands`
    concurrently, using a thread pool of `thread_count`.

    """

    def __init__(self, commands, thread_count=2):
        self.commands = list(commands)
        self.thread_count = thread_count

    def run(self):
        threads = []
        for command in self.commands:
            print '>>> Starting thread for command %r' % command
            t = Thread(target=command)
            threads.append(t)
            t.start()

            while len(threads) >= self.thread_count:
                sleep(1)
                threads = [thread for thread in threads if thread.is_alive()]

def main():
    """Console script entry point"""

    parser = ArgumentParser('cmdq')
    parser.add_argument('filename', help='Config filename.')
    args = parser.parse_args()

    with open(args.filename) as f:
        code = compile(f.read(), args.filename, 'exec')
        config = {}

    exec code in config
    if not 'cmdq' in config:
        raise Exception, 'Please provide a cmdq local in your config file.'

    CommandQueue(commands=config['cmdq']).run()
