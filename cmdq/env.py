from os import getenv as os_getenv

def getenv(varname, default=None):
    value = getenv(varname, help, default)

    if value is None:
        raise RuntimeError('You must set the %s environment variable. %s' % (varname, help, ))

    return value

