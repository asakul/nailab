
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qsci import *

from ui_gen.strategywidget import Ui_StrategyWidget

from ui.newdatasourcedialog import NewDataSourceDialog

ROLE_FEED_ID = QtCore.Qt.UserRole + 1

class StrategyWidget(QtWidgets.QWidget):

    def __init__(self, datasourcemanager, source_file, parent=None, content=None):
        super().__init__(parent)

        self.ui = Ui_StrategyWidget()
        self.ui.setupUi(self)

        self.source_file = source_file

        s = QtCore.QSettings()

        self.datasourcemanager = datasourcemanager
        self.datasourcemanager.load_sources(s)
        self.update_feeds_list()

        self.ui.splitter.setSizes([20, 80])
        self.ui.splitter.setStretchFactor(0, 1)
        self.ui.splitter.setStretchFactor(1, 1)

        font = QtGui.QFont("DejaVu Sans Mono")
        font.setPointSize(10)
        self.ui.editor.setFont(font)
        if content is not None:
            self.ui.editor.setText(content)

        lexer = QsciLexerPython()
        lexer.setFont(font)
        self.ui.editor.setLexer(lexer)
        self.ui.editor.setUtf8(True)

        self.result = []
        self.result_widget = None

        try:
            if s.value("time_window") is not None:
                (from_time, to_time) = s.value("time_window")
                self.ui.rb_timeWindow.setChecked(True)
                self.ui.dte_from.setDateTime(from_time)
                self.ui.dte_to.setDateTime(to_time)

            self.ui.splitter.restoreState(s.value("strategy_widget_splitter_state"))
            self.ui.splitter_editor.restoreState(s.value("strategy_widget_splitter_editor_state"))

        except Exception as e:
            print("Exception: ", e)

    def addDataSource(self):
        dlg = NewDataSourceDialog(self)
        if dlg.exec() == QtWidgets.QDialog.Accepted:
            self.datasourcemanager.add_source(dlg.get_data_source())
            self.update_feeds_list()

    def deleteDataSource(self):
        selected = self.ui.tw_feeds.selectedItems()
        for s in selected:
            if self.ui.tw_feeds.indexOfTopLevelItem(s) >= 0:
                name = s.data(0, ROLE_FEED_ID)
                if name is not None:
                    self.datasourcemanager.remove_source(name[0])
        self.update_feeds_list()

    def refreshDataSources(self):
        self.update_feeds_list()

    def save_state(self):
        s = QtCore.QSettings()
        self.datasourcemanager.save_sources(s)
        if self.ui.rb_allData.isChecked():
            s.setValue("time_window", None)
        else:
            s.setValue("time_window", (self.ui.dte_from.dateTime(), self.ui.dte_to.dateTime()))

        s.setValue("strategy_widget_splitter_state", self.ui.splitter.saveState())
        s.setValue("strategy_widget_splitter_editor_state", self.ui.splitter_editor.saveState())
        

    def save(self):
        with open(self.source_file, "w") as f:
            f.write(self.ui.editor.text())

    def get_time_window(self):
        if self.ui.rb_allData.isChecked():
            return None
        elif self.ui.rb_timeWindow.isChecked():
            return (self.ui.dte_from.dateTime(), self.ui.dte_to.dateTime())

    def update_feeds_list(self):
        self.ui.tw_feeds.clear()
        sources = self.datasourcemanager.all_sources()
        for source in sources:
            src_item = QtWidgets.QTreeWidgetItem(self.ui.tw_feeds)
            src_item.setText(0, source.name)
            src_item.setData(0, ROLE_FEED_ID, (source.name, ""))
            for feed in source.available_feeds():
                feed_item = QtWidgets.QTreeWidgetItem(src_item)
                feed_item.setText(0, feed)
                feed_item.setData(0, ROLE_FEED_ID, (source.name, feed))

    def get_selected_feeds(self):
        feeds = []
        items = self.ui.tw_feeds.selectedItems()
        for item in items:
            feeds.append(item.data(0, ROLE_FEED_ID))
        return feeds

    def set_result(self, result):
        self.result = result
        self.update_result()


    def update_result(self):
        if self.result_widget is None:
            self.result_widget = QtWidgets.QTreeWidget(self)
            self.ui.tabs.addTab(self.result_widget, "Result")

        rw = self.result_widget
        rw.clear()

        rw.setHeaderLabels(["", "Long", "Short", "All"])
        total_trades = QtWidgets.QTreeWidgetItem(self.result_widget)
        total_trades.setText(0, "Total trades")
        total_trades.setText(1, "{:d}".format(self.result[0]['long']['number_of_trades']))
        total_trades.setText(2, "{:d}".format(self.result[0]['short']['number_of_trades']))
        total_trades.setText(3, "{:d}".format(self.result[0]['all']['number_of_trades']))

        won_trades = QtWidgets.QTreeWidgetItem(self.result_widget)
        won_trades.setText(0, "Won trades")
        won_trades.setText(1, "{:d}".format(self.result[0]['long']['won']))
        won_trades.setText(2, "{:d}".format(self.result[0]['short']['won']))
        won_trades.setText(3, "{:d}".format(self.result[0]['all']['won']))

        lost_trades = QtWidgets.QTreeWidgetItem(self.result_widget)
        lost_trades.setText(0, "Lost trades")
        lost_trades.setText(1, "{:d}".format(self.result[0]['long']['lost']))
        lost_trades.setText(2, "{:d}".format(self.result[0]['short']['lost']))
        lost_trades.setText(3, "{:d}".format(self.result[0]['all']['lost']))

        net_profit = QtWidgets.QTreeWidgetItem(self.result_widget)
        net_profit.setText(0, "Net profit")
        net_profit.setText(1, "{:.3f}".format(self.result[0]['long']['net_profit']))
        net_profit.setText(2, "{:.3f}".format(self.result[0]['short']['net_profit']))
        net_profit.setText(3, "{:.3f}".format(self.result[0]['all']['net_profit']))

        total_won = QtWidgets.QTreeWidgetItem(self.result_widget)
        total_won.setText(0, "Total won")
        total_won.setText(1, "{:.3f}".format(self.result[0]['long']['total_won']))
        total_won.setText(2, "{:.3f}".format(self.result[0]['short']['total_won']))
        total_won.setText(3, "{:.3f}".format(self.result[0]['all']['total_won']))

        total_lost = QtWidgets.QTreeWidgetItem(self.result_widget)
        total_lost.setText(0, "Total lost")
        total_lost.setText(1, "{:.3f}".format(self.result[0]['long']['total_lost']))
        total_lost.setText(2, "{:.3f}".format(self.result[0]['short']['total_lost']))
        total_lost.setText(3, "{:.3f}".format(self.result[0]['all']['total_lost']))

        average_pnl = QtWidgets.QTreeWidgetItem(self.result_widget)
        average_pnl.setText(0, "Average pnl")
        average_pnl.setText(1, "{:.3f}".format(self.result[0]['long']['avg']))
        average_pnl.setText(2, "{:.3f}".format(self.result[0]['short']['avg']))
        average_pnl.setText(3, "{:.3f}".format(self.result[0]['all']['avg']))

        average_percentage = QtWidgets.QTreeWidgetItem(self.result_widget)
        average_percentage.setText(0, "Average %")
        average_percentage.setText(1, "{:.3f}".format(self.result[0]['long']['avg_percentage']))
        average_percentage.setText(2, "{:.3f}".format(self.result[0]['short']['avg_percentage']))
        average_percentage.setText(3, "{:.3f}".format(self.result[0]['all']['avg_percentage']))

        average_bars_in_trade = QtWidgets.QTreeWidgetItem(self.result_widget)
        average_bars_in_trade.setText(0, "Average bars in trade")
        average_bars_in_trade.setText(1, "{:.3f}".format(self.result[0]['long']['avg_bars']))
        average_bars_in_trade.setText(2, "{:.3f}".format(self.result[0]['short']['avg_bars']))
        average_bars_in_trade.setText(3, "{:.3f}".format(self.result[0]['all']['avg_bars']))

        profit_factor = QtWidgets.QTreeWidgetItem(self.result_widget)
        profit_factor.setText(0, "Profit factor")
        profit_factor.setText(1, "{:.3f}".format(self.result[0]['long']['profit_factor']))
        profit_factor.setText(2, "{:.3f}".format(self.result[0]['short']['profit_factor']))
        profit_factor.setText(3, "{:.3f}".format(self.result[0]['all']['profit_factor']))

        self.result_widget.resizeColumnToContents(0)

    def setError(self, errmsg):
        self.ui.te_notes.clear()
        self.ui.te_notes.appendPlainText(errmsg)

