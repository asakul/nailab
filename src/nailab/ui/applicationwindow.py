
from gi.repository import Gtk, GtkSource

class ApplicationWindow:

    def __init__(self, builder):
        self.window = builder.get_object('ApplicationWindow')
        manager = GtkSource.LanguageManager()
        buf = GtkSource.Buffer()
        buf.set_language(manager.get_language('python'))
        sv = builder.get_object('sourceview')
        sv.set_buffer(buf)
        sv.set_monospace(True)

        handlers = {
                'on_ApplicationWindow_delete_event' : Gtk.main_quit
                }

        builder.connect_signals(handlers)
        self.window.show_all()

