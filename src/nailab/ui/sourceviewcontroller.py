
class SourceViewController:

    def __init__(self, sourceview):
        self.sourceview = sourceview

    def set_source_text(self, text):
        self.sourceview.get_buffer().set_text(text)

    def get_source_text(self):
        buf = self.sourceview.get_buffer()
        return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
        
