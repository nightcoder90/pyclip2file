from PySide2.QtWidgets import QWidget, QGroupBox

class EditorPanelMixin:
    def __init__(self, key: str):
        self._key: str = key

    @property
    def key(self):
        return self._key


class EditorPanel(QWidget, EditorPanelMixin):
    """
    Base class for editor panels.
    """

    def __init__(self, key: str):
        QWidget.__init__(self)
        EditorPanelMixin.__init__(self, key)


class GroupBoxEditorPanel(QGroupBox, EditorPanelMixin):
    """
    Base class for editor panels.
    """

    def __init__(self, key: str):
        QGroupBox.__init__(self)
        EditorPanelMixin.__init__(self, key)
