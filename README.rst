cmdq
====

Simple command queue. Given a list of python callable, creates a thread pool to
unstack them concurrently.

The only dependency it has is python2.7 and python-setuptools. To install in on
an ubuntu system for example, use the following::

    apt-get install -y python2.7 python-setuptools
    update-alternatives --install /usr/bin/python python2.7 /usr/bin/python2.7 10

Download
::::::::

From github::

    git clone git://github.com/maisonsdumonde/cmdq.git
    cd cmdq

Install in a virtualenv
:::::::::::::::::::::::

Isolating your cmdq in a virtualenv is highly encouraged::

    virtualenv .py-env
    . .py-env/bin/activate
    python setup.py develop

Install globally in the system
::::::::::::::::::::::::::::::

No fear? Install globally::

    sudo python setup.py install

Syntax
::::::

Run a cmdq file::

    cmdq example/simple.cmdq

For cmdq file syntax, it's mostly python, and loader looks for a "cmdq"
attribute which must be a list of your python callables to dispatch in
threads.

Config
::::::

For each command queue, create a .cmdq file using python syntax. The only
requirement is that it defines a cmdq local containing an iterable of the
python callables it needs to run. You can look at examples in example
directory.

Resource pools
::::::::::::::

Sometimes, workers share a limited set of resources (for example, slave boxes
that will run the actual code). You can use a ResourcePool to achieve this. The
worker will wait for an availabl thread, and an availabl resource, to be run.
For now, you should avoid to use more than one resource pool for a given
worker, you may end up in a deadlock situation::

    servers = ResourcePool('web-1', 'web-2')

    @servers.use
    def my_worker(server):
        print server

    # ...

Global initializer/finalizer
::::::::::::::::::::::::::::

Sometimes it's handy to execute something before any cmdq is started, or after
all cmdq finished execution::

    def initialize():
        system('echo I am the first!')

    def finalize():
        system('echo I am the last!')

License
:::::::

Copyright (C) 2012 Maisons du Monde

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
