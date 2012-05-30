from time import sleep

class ResourcePool(object):
    def __init__(self, *resources, **kwargs):
        self.resources = list(resources)
        self.initializer = 'initializer' in kwargs and kwargs['initializer'] or None
        self.finalizer = 'finalizer' in kwargs and kwargs['finalizer'] or None

    def initialize(self):
        if callable(self.initializer):
            for resource in self.resources:
                print '>>> Initialize resource "%r".' % (resource, )
                self.initializer(resource)

    def finalize(self):
        if callable(self.finalizer):
            for resource in self.resources:
                print '>>> Finalize resource "%r".' % (resource, )
                self.finalizer(resource)

    def pop(self):
        if not len(self.resources):
            raise RuntimeError('No resource available in this pool.')

        return self.resources.pop(0)

    def push(self, resource):
        self.resources.append(resource)

    def __len__(self):
        return len(self.resources)

    def use(self, wrapped):
        """Decorator used to mark a worker as needing an exclusive lock on this
        resource.

        """

        def wrapper():
            while not len(self): sleep(1)
            resource = self.pop()
            print '>>> LOCK resource "%r".' % (resource, )
            retval = wrapped(resource)
            print '>>> UNLOCK resource "%r".' % (resource, )
            self.push(resource)
            return retval

        wrapper.__name__ = wrapped.__name__
        return wrapper

