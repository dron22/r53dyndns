
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


class Tox(TestCommand):

    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

setup(
    name='r53dyndns',
    version='0.1',
    description='Simple DynDns with AWS Route53',
    url='https://github.com/dron22/r53dyndns',
    author='dron22',
    author_email='info@fastback.io',
    license='MIT',
    packages=['r53dyndns'],
    install_requires=requirements,
    scripts=['bin/r53dyndns'],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    zip_safe=False
)
