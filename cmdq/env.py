from os import getenv as os_getenv

def getenv(varname, help, default=None):
    value = os_getenv(varname, default)

    if value is None:
        raise RuntimeError('You must set the %s environment variable. %s' % (varname, help, ))

    return value

