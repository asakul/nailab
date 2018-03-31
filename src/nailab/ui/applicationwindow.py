
from gi.repository import Gtk, GtkSource

from nailab.data.datasourcemanager import DataSourceManager
from .sourceviewcontroller import SourceViewController

class ApplicationWindow:

    def __init__(self, builder):
        self.window = builder.get_object('ApplicationWindow')
        self._init_sourceeditor(builder)

        self._init_tv_datasource(builder)

        handlers = {
                'on_ApplicationWindow_delete_event' : Gtk.main_quit,
                'on_OpenFile' : self.open_file
                }

        builder.connect_signals(handlers)
        self.window.show_all()

    def open_file(self, arg):
        dlg = Gtk.FileChooserDialog('Open file', self.window, Gtk.FileChooserAction.OPEN,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        result = dlg.run()

        if result == Gtk.ResponseType.OK:
            with open(dlg.get_filename(), 'r') as f:
                self.sourceviewcontroller.set_source_text(f.read())


        dlg.destroy()


    def _init_sourceeditor(self, builder):
        manager = GtkSource.LanguageManager()
        buf = GtkSource.Buffer()
        buf.set_language(manager.get_language('python'))
        sv = builder.get_object('sourceview')
        sv.set_buffer(buf)
        sv.set_monospace(True)
        
        self.sourceviewcontroller = SourceViewController(sv)

    def _init_tv_datasource(self, builder):
        self.datasourcemanager = DataSourceManager()
        self.datasourcemanager.load_sources()

        tv_datasources = builder.get_object('tv_datasources')

        self.datasources_store = Gtk.TreeStore(str)
        for source in self.datasourcemanager.all_sources():
            treeiter = self.datasources_store.append(None, (source.name,))
            for feed in source.available_feeds():
                self.datasources_store.append(treeiter, (feed,))
                

        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Datasources', rendererText, text=0)
        tv_datasources.append_column(column)

        tv_datasources.set_model(self.datasources_store)

