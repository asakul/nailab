
from gi.repository import Gtk

from prettytable import PrettyTable

from .equitygraph import EquityGraph

def render_float(a):
    return "{:.3f}".format(a)

def render_ratio(a, b):
    if b != 0:
        return a / b
    else:
        return "∞"

class ResultsTableWidget(Gtk.Notebook):

    def __init__(self):
        super().__init__()

        self.set_tab_pos(Gtk.PositionType.LEFT)

        self.buffer = Gtk.TextBuffer()
        self.text_result = Gtk.TextView()
        self.text_result.set_buffer(self.buffer)
        self.append_page(self.text_result, Gtk.Label('Statistics'))

        self.equity_graph = EquityGraph()
        self.append_page(self.equity_graph, Gtk.Label('Equity'))

        style_ctx = self.text_result.get_style_context()
        self.provider = Gtk.CssProvider()
        self.provider.load_from_data(b'GtkTextView { font-family: "Monospace"; }')
        style_ctx.add_provider(self.provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def set_results(self, results, trades):
        self.buffer.set_text(self.generate_plain_text(results))
        self.equity_graph.set_trades(trades)

    def generate_plain_text(self, stats):

        table = PrettyTable()
        table.field_names = ["", "All positions", "Long only", "Short only"]
        table.add_row(["Net profit", render_float(stats['all']['net_profit']), render_float(stats['long']['net_profit']), render_float(stats['short']['net_profit'])])
        table.add_row(["Bars in trade", stats['all']['bars_in_trade'], stats['long']['bars_in_trade'], stats['short']['bars_in_trade']])
        table.add_row(["Profit per bar", render_float(stats['all']['profit_per_bar']), render_float(stats['long']['profit_per_bar']), render_float(stats['short']['profit_per_bar'])])
        table.add_row(["Number of trades", stats['all']['number_of_trades'], stats['long']['number_of_trades'], stats['short']['number_of_trades']])
        table.add_row(["Avg. profit", render_float(stats['all']['avg']), render_float(stats['long']['avg']), render_float(stats['short']['avg'])])
        table.add_row(["Avg. profit, %", render_float(stats['all']['avg_percentage']), render_float(stats['long']['avg_percentage']), render_float(stats['short']['avg_percentage'])])
        table.add_row(["Avg. bars in trade", render_float(stats['all']['avg_bars']), render_float(stats['long']['avg_bars']), render_float(stats['short']['avg_bars'])])
        table.add_row(["Winning trades", stats['all']['won'], stats['long']['won'], stats['short']['won']])
        table.add_row(["Gross profit", render_float(stats['all']['total_won']), render_float(stats['long']['total_won']), render_float(stats['short']['total_won'])])
        table.add_row(["Losing trades", stats['all']['lost'], stats['long']['lost'], stats['short']['lost']])
        table.add_row(["Gross loss", render_float(stats['all']['total_lost']), render_float(stats['long']['total_lost']), render_float(stats['short']['total_lost'])])
        table.add_row(["Profit factor", render_float(stats['all']['profit_factor']), render_float(stats['long']['profit_factor']), render_float(stats['short']['profit_factor'])])

        return table.get_string()

