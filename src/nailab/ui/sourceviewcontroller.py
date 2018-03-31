
class SourceViewController:

    def __init__(self, sourceview):
        self.sourceview = sourceview

    def set_source_text(self, text):
        self.sourceview.get_buffer().set_text(text)
