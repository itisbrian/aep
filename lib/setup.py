from distutils.core import setup, Command

setup(
    name='aep_gfb',
    version='0.0.1',
    packages=['aep_gfb'],
    url='https://gitlab.bnet/patrickg/green_fireball',
    install_requires=[],   #We should probably insert the other stuff here; but whatever.
    license='Proprietary',
    author='Patrick Geary',
    author_email='patrickg@supermicro.com',
    description='Python module for interfacing with ndctl and ipmctl for AEP DIMM Control and Management',
    cmdclass={},
)

