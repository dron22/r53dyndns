from setuptools import setup

setup(
    name='r53dyndns',
    version='0.1',
    description='Simple DynDns with AWS Route53',
    url='https://github.com/dron22/r53dyndns',
    author='dron22',
    author_email='info@fastback.io',
    license='MIT',
    packages=['r53dyndns'],
    install_requires=[
        'boto==2.39.0',
        'requests==2.9.1',
    ],
    zip_safe=False
)
