
import os.path
import datetime
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qsci import *

from ui_gen.strategywidget import Ui_StrategyWidget

from ui.newdatasourcedialog import NewDataSourceDialog
from ui.equitychartwidget import EquityChartWidget
from ui.tradeslistwidget import TradesListWidget
from ui.statisticwidget import StatisticWidget

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

ROLE_FEED_ID = QtCore.Qt.UserRole + 1

class FileModifiedHandler(FileSystemEventHandler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def on_modified(self, event):
        self.callback(event.src_path)
        

class StrategyWidget(QtWidgets.QWidget):

    savedChanged = QtCore.pyqtSignal(name="savedChanged")

    def __init__(self, datasourcemanager, source_file, parent=None, content=None):
        super().__init__(parent)

        self.ui = Ui_StrategyWidget()
        self.ui.setupUi(self)

        self.saved = False
        self.save_timestamp = datetime.datetime.now()

        self.ui.editor.textChanged.connect(self.editorTextChanged)

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
            fixed_content = "\n".join(content.splitlines())
            self.ui.editor.setText(fixed_content)

        self.ui.editor.setIndentationsUseTabs(False)
        self.ui.editor.setTabWidth(4)
        self.ui.editor.setAutoIndent(True)

        self.source_file = source_file
        if self.source_file is not None:
            self.saved = True


        lexer = QsciLexerPython()
        lexer.setFont(font)
        self.ui.editor.setLexer(lexer)
        self.ui.editor.setUtf8(True)

        self.result = []
        self.result_widget = None
        self.equity_widget = None
        self.trades_widget = None
        self.statistic_widget = None

        self.watchdog_handler = FileModifiedHandler(self.file_modified)
        self.watchdog = None
        self.update_watchdog()

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

    def widget_type(self):
        return "strategy"

    def is_saved(self):
        return self.saved

    def editorTextChanged(self):
        saved = self.saved
        self.saved = False
        if saved:
            self.savedChanged.emit()

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
        self.save_timestamp = datetime.datetime.now()
        with open(self.source_file, "w") as f:
            f.write(self.ui.editor.text())
            saved = self.saved
            self.saved = True
            if not saved:
                self.savedChanged.emit()

    def save_as(self, source_file):
        self.source_file = source_file
        self.save_timestamp = datetime.datetime.now()
        with open(self.source_file, "w") as f:
            f.write(self.ui.editor.text())
            saved = self.saved
            self.saved = True
            if not saved:
                self.savedChanged.emit()
        

    def get_time_window(self):
        if self.ui.rb_allData.isChecked():
            return None
        elif self.ui.rb_timeWindow.isChecked():
            return (self.ui.dte_from.dateTime(), self.ui.dte_to.dateTime())

    def update_feeds_list(self):
        self.ui.tw_feeds.clear()
        sources = self.datasourcemanager.all_sources()
        for source in sources:
            source.refresh()
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
        self.update_equity_chart()
        self.update_trades_list()


    def update_equity_chart(self):
        pnl = [x['pnl'] for x in self.result[1]]
        cumpnl = np.cumsum(pnl)
        drawdown = []
        cur_max = 0
        drawdown_lengths = []
        cur_drawdown = 0
        cur_drawdown_max = 0
        for i in range(0, len(cumpnl)):
            if cumpnl[i] > cur_max:
                cur_max = cumpnl[i]
                drawdown.append(0)
                if cur_drawdown > 0:
                    drawdown_lengths.append((cur_drawdown, cur_drawdown_max))
                cur_drawdown = 0
                cur_drawdown_max = 0
            else:
                drawdown.append(-(cur_max - cumpnl[i]))
                cur_drawdown += 1
                cur_drawdown_max = max(cur_drawdown_max, cur_max - cumpnl[i])
        if self.equity_widget is None:
            self.equity_widget = EquityChartWidget(self)
            self.ui.tabs.addTab(self.equity_widget, "Equity")

        #self.equity_widget.set_data(self.result[2])
        self.equity_widget.set_data(cumpnl, np.array(drawdown))

        print(drawdown_lengths)

    def update_trades_list(self):
        if self.trades_widget is None:
            self.trades_widget = TradesListWidget(self)
            self.ui.tabs.addTab(self.trades_widget, "Trades")

        if self.statistic_widget is None:
            self.statistic_widget = StatisticWidget(self)
            self.ui.tabs.addTab(self.statistic_widget, "Statistic")

        self.trades_widget.set_trades(self.result[1])
        self.statistic_widget.set_trades(self.result[1])

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

        won_percentage = QtWidgets.QTreeWidgetItem(self.result_widget)
        won_percentage.setText(0, "% profitable")
        won_percentage.setText(1, "{:.2f}".format(100 * self._ratio(self.result[0]['long']['won'], self.result[0]['long']['won'] + self.result[0]['long']['lost'])))
        won_percentage.setText(2, "{:.2f}".format(100 * self._ratio(self.result[0]['short']['won'], self.result[0]['short']['won'] + self.result[0]['short']['lost'])))
        won_percentage.setText(3, "{:.2f}".format(100 * self._ratio(self.result[0]['all']['won'], self.result[0]['all']['won'] + self.result[0]['all']['lost'])))

        net_profit = QtWidgets.QTreeWidgetItem(self.result_widget)
        net_profit.setText(0, "Net profit")
        net_profit.setText(1, "{:.3f}".format(self.result[0]['long']['net_profit']))
        net_profit.setText(2, "{:.3f}".format(self.result[0]['short']['net_profit']))
        net_profit.setText(3, "{:.3f}".format(self.result[0]['all']['net_profit']))

        total_commission = QtWidgets.QTreeWidgetItem(self.result_widget)
        total_commission.setText(0, "Total commission")
        total_commission.setText(1, "{:.3f}".format(self.result[0]['long']['total_commission']))
        total_commission.setText(2, "{:.3f}".format(self.result[0]['short']['total_commission']))
        total_commission.setText(3, "{:.3f}".format(self.result[0]['all']['total_commission']))

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

        sharpe_ratio = QtWidgets.QTreeWidgetItem(self.result_widget)
        sharpe_ratio.setText(0, "Z-score")
        sharpe_ratio.setText(1, "{:.3f}".format(self.result[0]['long']['z_score']))
        sharpe_ratio.setText(2, "{:.3f}".format(self.result[0]['short']['z_score']))
        sharpe_ratio.setText(3, "{:.3f}".format(self.result[0]['all']['z_score']))

        t_stat = QtWidgets.QTreeWidgetItem(self.result_widget)
        t_stat.setText(0, "t-statistics")
        t_stat.setText(1, "{:.3f}".format(self.result[0]['long']['t_stat']))
        t_stat.setText(2, "{:.3f}".format(self.result[0]['short']['t_stat']))
        t_stat.setText(3, "{:.3f}".format(self.result[0]['all']['t_stat']))

        kelly = QtWidgets.QTreeWidgetItem(self.result_widget)
        kelly.setText(0, "Kelly ratio")
        kelly.setText(1, "{:.1f}%".format(100. * self.result[0]['long']['kelly']))
        kelly.setText(2, "{:.1f}%".format(100. * self.result[0]['short']['kelly']))
        kelly.setText(3, "{:.1f}%".format(100. * self.result[0]['all']['kelly']))

        self.result_widget.resizeColumnToContents(0)

    def setError(self, errmsg):
        self.ui.te_notes.clear()
        self.ui.te_notes.appendPlainText(errmsg)

    def update_watchdog(self):
        if self.watchdog is not None:
            self.watchdog.stop()
            self.watchdog.join()

        if self.source_file is not None:
            self.watchdog = Observer()
            self.watchdog.schedule(self.watchdog_handler, os.path.dirname(self.source_file), recursive=False)
            self.watchdog.start()

    def file_modified(self, fname):
        try:
            if datetime.datetime.now() - self.save_timestamp > datetime.timedelta(seconds=2):
                if self.source_file is not None and os.path.samefile(self.source_file, fname):
                    with open(self.source_file, "r") as f:
                        self.ui.editor.setText(f.read())
        except:
            # Saving file from the outside generates a lot of events, as temporary and backup files are created and removed.
            # Hence, we ignore errors
            pass


    def _ratio(self, a, b):
        if b == 0:
            return 0
        else:
            return float(a) / b
