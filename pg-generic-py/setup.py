from distutils.core import setup, Command

setup(
    name='pggenericpy',
    version='0.0.2',
    packages=['pggenericpy'],
    url='https://gitlab.bnet/patrickg/pg-generic-py',
    install_requires=[],
    license='MIT',
    author='Patrick Geary',
    author_email='patrickg@supermicro.com',
    description='Small python module for handling my super-generic, always-used calls.',
    cmdclass={},
)
