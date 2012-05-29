from time import sleep

class ResourcePool(object):
    def __init__(self, *resources):
        self.resources = list(resources)

    def pop(self):
        if not len(self.resources):
            raise RuntimeError('No resource available in this pool.')

        return self.resources.pop()

    def push(self, resource):
        self.resources.append(resource)

    def __len__(self):
        return len(self.resources)

    def use(self, wrapped):
        def wrapper():
            while not len(self): sleep(1)
            resource = self.pop()
            retval = wrapped(resource)
            self.push(resource)
            return retval

        wrapper.__name__ = wrapped.__name__
        return wrapper

