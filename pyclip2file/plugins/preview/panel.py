from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QVBoxLayout
from pyclip2file.plugins.editor.editorpanel import GroupBoxEditorPanel
from pyclip2file.widgets.pixmapviewer import PixmapViewer


class PreviewPanel(GroupBoxEditorPanel):
    def __init__(self):
        GroupBoxEditorPanel.__init__(self, 'A.Preview')
        self.setTitle('Preview')
        lyt = QVBoxLayout()
        #lyt.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(lyt)
        self._viewer = PixmapViewer()
        lyt.addWidget(self._viewer)

    def setPixmap(self, pixmap: QPixmap):
        self._viewer.setPixmap(pixmap)
