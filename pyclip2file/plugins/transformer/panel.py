from pyclip2file.plugins.editor.editorpanel import GroupBoxEditorPanel


class TransformerPanel(GroupBoxEditorPanel):
    def __init__(self):
        GroupBoxEditorPanel.__init__(self, 'C.Transform')
        self.setTitle('Transform')