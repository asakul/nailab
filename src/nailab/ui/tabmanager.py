
from gi.repository import GObject, Gtk, GtkSource, Pango

from .sourceviewcontroller import SourceViewController

class TabManager(GObject.Object):

    def __init__(self, notebook):
        super().__init__()
        self.notebook = notebook
        self.widgets = {}

    def new_tab(self, source_file):
        with open(source_file, 'r') as f:
            (sv, sv_controller) = self._init_sourceeditor()
            sv_controller.set_source_text(f.read())
            self.widgets[source_file] = sv
            sv.show_all()
            header = Gtk.HBox()
            title_label = Gtk.Label(source_file)
            image = Gtk.Image()
            image.set_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)
            close_button = Gtk.Button()
            close_button.set_image(image)
            close_button.set_relief(Gtk.ReliefStyle.NONE)
            close_button.connect('clicked', self.close_cb, source_file)

            header.pack_start(title_label,
                              expand=True, fill=True, padding=0)
            header.pack_end(close_button,
                            expand=False, fill=False, padding=0)
            header.show_all()
            index = self.notebook.append_page(sv, header)
            self.notebook.set_current_page(index)

    def close_cb(self, arg, source_file):
        index = self._widget_num_by_source_file(source_file)
        self.notebook.remove_page(index)
        del self.widgets[source_file]

    def get_current_source_path(self):
        index = self.notebook.get_current_page()
        w = self.notebook.get_nth_page(index)
        for k, v in self.widgets.items():
            if v == w:
                return k

        raise KeyError('Invalid widget')

    def _init_sourceeditor(self):
        scroll = Gtk.ScrolledWindow()
        manager = GtkSource.LanguageManager()
        buf = GtkSource.Buffer()
        buf.set_language(manager.get_language('python'))
        sv = GtkSource.View()
        sv.set_buffer(buf)
        sv.set_monospace(True)

        style_ctx = sv.get_style_context()
        self.provider = Gtk.CssProvider()
        self.provider.load_from_data(b'GtkSourceView { font-family: "Monospace"; }')
        style_ctx.add_provider(self.provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        sourceviewcontroller = SourceViewController(sv)
        scroll.add(sv)
        scroll.show()

        return (scroll, sourceviewcontroller)

    def _widget_num_by_source_file(self, source_file):
        for i in range(0, self.notebook.get_n_pages()):
            if self.widgets[source_file] == self.notebook.get_nth_page(i):
                return i
        return None
