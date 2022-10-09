from setuptools import setup, find_packages
import os

setup(
    name='pyclip2file',
    version='0.1',
    description='PyClip2File is a program that saves clipboard images to files.',
    author='nightcoder90',
    author_email='nightcoder90@gmail.com',
    packages=find_packages(),
    entry_points={
        'gui_scripts': [
            'pyclip2file = pyclip2file.app.start:main'
        ]
    },
    install_requires= [
        'PySide2>=5.10.0',
    ]
)