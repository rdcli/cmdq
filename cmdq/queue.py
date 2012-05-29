from threading import Thread
from time import sleep

class CommandQueue(object):
    """Class to configure a command queue, that will run `commands`
    concurrently, using a thread pool of `thread_count` threads.

    """

    def __init__(self, commands, thread_count):
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

