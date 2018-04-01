
from gi.repository import Gtk, GtkSource

from nailab.data.datasource import DataSource
from nailab.data.datasourcemanager import DataSourceManager
from nailab.execution.executor import Executor

from .resultstable import ResultsTableWidget
from .tabmanager import TabManager

class ApplicationWindow:

    def __init__(self, builder):
        self.window = builder.get_object('ApplicationWindow')
        self.tab_manager = TabManager(builder.get_object('sourceNotebook'))

        self._init_tv_datasource(builder)

        handlers = {
                'on_ApplicationWindow_delete_event' : Gtk.main_quit,
                'on_OpenFile' : self.open_file,
                'on_StrategyExecute' : self.strategy_execute
                }

        builder.connect_signals(handlers)
        self.window.show_all()

    def open_file(self, arg):
        dlg = Gtk.FileChooserDialog('Open file', self.window, Gtk.FileChooserAction.OPEN,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        result = dlg.run()

        if result == Gtk.ResponseType.OK:
            self.tab_manager.new_tab(dlg.get_filename())

        dlg.destroy()

    def strategy_execute(self, arg):
        sel = self.tv_datasources.get_selection()
        model, rows = sel.get_selected_rows()

        feeds = []
        for row in rows:
            (feed_id, source_name) = self.datasources_store.get(self.datasources_store.get_iter(row), 0, 1)
            source = self.datasourcemanager.get_source(source_name)
            if source is not None:
                feed = source.get_feed(feed_id)
                feeds.append(feed)

        e = Executor()
        result = e.execute_from_file(self.tab_manager.get_current_source_path(), feeds)

        self._add_results_page(result)

    def _add_results_page(self, results):
        res_widget = ResultsTableWidget()
        res_widget.set_results(results)
        res_widget.show_all()
        self.tab_manager.new_misc_tab(res_widget)

    def _init_tv_datasource(self, builder):
        self.datasourcemanager = DataSourceManager()
        self.datasourcemanager.load_sources()

        tv_datasources = builder.get_object('tv_datasources')
        self.tv_datasources = tv_datasources

        self.datasources_store = Gtk.TreeStore(str, str)
        for source in self.datasourcemanager.all_sources():
            treeiter = self.datasources_store.append(None, (source.name, source.name))
            for feed in source.available_feeds():
                self.datasources_store.append(treeiter, (feed, source.name))
                

        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Datasources', rendererText, text=0)
        tv_datasources.append_column(column)

        tv_datasources.set_model(self.datasources_store)

        sel = tv_datasources.get_selection()
        sel.set_mode(Gtk.SelectionMode.MULTIPLE)



