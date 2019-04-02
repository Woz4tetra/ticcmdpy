from setuptools import setup, find_packages

setup(
    name='ticcmdpy',
    version='0.1.dev0',
    packages=find_packages(),
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    install_requires=[
      'pyserial',
  ]
)
