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
            'clipboard_view = pyclip2file.plugins.clipboardview.plugin:ClipboardViewPlugin',
            'clipboard_watcher = pyclip2file.plugins.clipboardwatcher.plugin:ClipboardWatcherPlugin',
            'editor = pyclip2file.plugins.editor.plugin:EditorPlugin',
            'file_exporter = pyclip2file.plugins.fileexporter.plugin:FileExporterPlugin',
            'postprocessor = pyclip2file.plugins.postprocessor.plugin:PostProcessorPlugin',
            'preview = pyclip2file.plugins.preview.plugin:PreviewPlugin',
            'scale_transformer = pyclip2file.plugins.scaletransformer.plugin:ScaleTransformerPlugin',
            'transformer = pyclip2file.plugins.transformer.plugin:TransformerPlugin',
        ]
    },
    install_requires= [
        'PySide2>=5.10.0',
    ]
)