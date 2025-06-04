from setuptools import setup, find_packages

setup(
    name='robot_pbd',
    version='0.0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'}
)
