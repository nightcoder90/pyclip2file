from setuptools import setup, find_packages
import os

setup(
    name='pyclip2file',
    version='0.1',
    description='Pyclip2file is a program that saves clipboard images to files.',
    author='nightcoder90',
    author_email='nightcoder90@gmail.com',
    packages=find_packages(),
    entry_points={
        'gui_scripts': [
            'pyclip2file = pyclip2file.app.start:main'
        ],
        'pyclip2file.plugins': [
            'clipboard = pyclip2file.plugins.clipboard.plugin:ClipboardPlugin',
            'editor = pyclip2file.plugins.editor.plugin:EditorPlugin',
            'file_saver = pyclip2file.plugins.filesaver.plugin:FileSaverPlugin',
            'preview = pyclip2file.plugins.preview.plugin:PreviewPlugin',
            'scaler = pyclip2file.plugins.scaler.plugin:ScalerPlugin',
        ]
    },
    install_requires= [
        'PySide2>=5.10.0',
    ]
)