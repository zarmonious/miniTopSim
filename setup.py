from setuptools import setup, find_packages

setup(
    name='mini_topsim',
    packages=find_packages(where='.'),
    package_dir={'': '.'},
    package_data={'mini_topsim': ['parameters.db', 'tables/*']},
    install_requires=['numpy', 'scipy', 'matplotlib']
)
