from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel
from pyclip2file.plugins.editor.editorpanel import EditorPanelMixin


class EditorWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.editor_panels = []
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

    def add_panel(self, editor_panel):
        assert isinstance(editor_panel, QWidget) and isinstance(editor_panel, EditorPanelMixin)
        self.editor_panels.append(editor_panel)
        self.editor_panels.sort(key=lambda p: p.key)
        idx = self.editor_panels.index(editor_panel)
        self._layout.insertWidget(idx, editor_panel)