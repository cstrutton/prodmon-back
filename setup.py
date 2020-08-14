from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='prodmon',
    version='0.1.0',
    description='A simple server to read PLC tags and post to an SQL database',
    long_description=readme,
    author='Chris Strutton',
    author_email='chris@rodandfly.ca',
    # url='https://github.com/kennethreitz/samplemod',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
