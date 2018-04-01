
from gi.repository import GObject, Gtk, GtkSource, Pango

from .sourceviewcontroller import SourceViewController

class TabManager(GObject.Object):

    def __init__(self, notebook):
        super().__init__()
        self.notebook = notebook
        self.widgets = {}
        self.source_controllers = {}
        self.id_counter = 1
        self.source_paths = {}

    def new_misc_tab(self, widget):
        tab_id = self._next_tab_id()
        self.widgets[tab_id] = widget
        header = Gtk.HBox()
        title_label = Gtk.Label('Result')
        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)
        close_button = Gtk.Button()
        close_button.set_image(image)
        close_button.set_relief(Gtk.ReliefStyle.NONE)
        close_button.connect('clicked', self.close_cb, tab_id)

        header.pack_start(title_label,
                          expand=True, fill=True, padding=0)
        header.pack_end(close_button,
                        expand=False, fill=False, padding=0)
        header.show_all()

        index = self.notebook.append_page(widget, header)
        self.notebook.set_current_page(index)

    def new_tab(self, source_file):
        with open(source_file, 'r') as f:
            tab_id = self._next_tab_id()
            self.source_paths[tab_id] = source_file
            (sv, sv_controller) = self._init_sourceeditor()
            sv_controller.set_source_text(f.read())
            self.source_controllers[tab_id] = sv_controller
            self.widgets[tab_id] = sv
            sv.show_all()
            header = Gtk.HBox()
            title_label = Gtk.Label(source_file)
            image = Gtk.Image()
            image.set_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)
            close_button = Gtk.Button()
            close_button.set_image(image)
            close_button.set_relief(Gtk.ReliefStyle.NONE)
            close_button.connect('clicked', self.close_cb, tab_id)

            header.pack_start(title_label,
                              expand=True, fill=True, padding=0)
            header.pack_end(close_button,
                            expand=False, fill=False, padding=0)
            header.show_all()
            index = self.notebook.append_page(sv, header)
            self.notebook.set_current_page(index)

    def close_cb(self, arg, tab_id):
        index = self._widget_num_by_tab_id(tab_id)
        self.notebook.remove_page(index)
        del self.widgets[tab_id]
        if tab_id in self.source_paths:
            del self.source_paths[tab_id]
        if tab_id in self.source_controllers:
            del self.source_controllers[tab_id]

    def get_current_source_path(self):
        index = self.notebook.get_current_page()
        w = self.notebook.get_nth_page(index)
        for k, v in self.widgets.items():
            if v == w:
                return self.source_paths[k]

        return None

    def save_current(self):
        index = self.notebook.get_current_page()
        w = self.notebook.get_nth_page(index)
        for k, v in self.widgets.items():
            if v == w:
                text = self.source_controllers[k].get_source_text()
                with open(self.source_paths[k], 'w') as f:
                    f.write(text)

    def save_current_as(self, path):
        index = self.notebook.get_current_page()
        w = self.notebook.get_nth_page(index)
        for k, v in self.widgets.items():
            if v == w:
                text = self.source_controllers[k].get_source_text()
                with open(path, 'w') as f:
                    f.write(text)

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

    def _widget_num_by_tab_id(self, tab_id):
        for i in range(0, self.notebook.get_n_pages()):
            if self.widgets[tab_id] == self.notebook.get_nth_page(i):
                return i
        return None

    def _next_tab_id(self):
        self.id_counter += 1
        return self.id_counter
