import logging
from typing import Optional
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import QPlainTextEdit, QLabel
from pyclip2file.widgets.layoutbuilder import LayoutBuilder

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class PostProcessorEngine(QObject):
    def __init__(self, parent: QObject=None) -> None:
        self._format = ''
        self._result = ''
        self._format_editor: Optional[QPlainTextEdit] = None
        self._result_viewer: Optional[QPlainTextEdit] = None

    def add_to_layout(self, layout_builder: LayoutBuilder):
        layout_builder.add_widget(QLabel('Format:'))
        layout_builder.finish_row()
        if not self._format_editor:
            self._format_editor = QPlainTextEdit()
        layout_builder.add_widget(self._format_editor)
        layout_builder.finish_row()

        layout_builder.add_widget(QLabel('Result:'))
        layout_builder.finish_row()
        if not self._result_viewer:
            self._result_viewer = QPlainTextEdit()
            self._result_viewer.setReadOnly(True)
        layout_builder.add_widget(self._result_viewer)
        layout_builder.finish_row()

    def process(self, path: str) -> None:
        self._format = self._format_editor.toPlainText()
        import os

        # /path/to/file.txt
        # %{0}: /path/to/file.txt
        # %{1}, %{-3}: path
        # %{2}, %{-2}: to
        # %{3}, %{-1}: file.txt
        path = os.path.normpath(path)
        replace_map = {'%{0}': path}
        for idx, token in enumerate(path.split(os.sep)):
            replace_map['%{' + str(idx+1) + '}'] = token
        for idx, token in enumerate(path.split(os.sep)[::-1]):
            replace_map['%{' + str(-idx-1) + '}'] = token
        
        self._result = self._format
        for k in replace_map:
            v = replace_map[k]
            self._result = self._result.replace(k, v)
        
        self._result_viewer.setPlainText(self._result)
