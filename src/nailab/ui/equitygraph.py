
from gi.repository import Gtk

class EquityGraph(Gtk.Misc):
    
    def __init__(self):
        super().__init__()
        self.trades = []
        self.cumulative_pnl = []

    def do_draw(self, cr):
        bg_color = self.get_style_context().get_background_color(Gtk.StateFlags.NORMAL)
        cr.set_source_rgba(*list(bg_color))
        cr.paint()

        allocation = self.get_allocation()
        if len(self.cumulative_pnl) > 0:
            fg_color = self.get_style_context().get_color(Gtk.StateFlags.NORMAL)
            cr.set_source_rgba(*list(fg_color));
            cr.set_line_width(2)

            min_equity = min(self.cumulative_pnl)
            max_equity = max(self.cumulative_pnl)

            kx = allocation.width / len(self.cumulative_pnl)
            ky = 0.8 * allocation.height / (max_equity - min_equity)

            cr.move_to(0, allocation.height * 0.9 - (self.cumulative_pnl[0] - min_equity) * ky)
            for i, x in enumerate(self.cumulative_pnl[1:]):
                cr.line_to((i + 1) * kx, allocation.height * 0.9 - (x - min_equity) * ky)
            cr.stroke()        

    def set_trades(self, trades):
        self.trades = trades
        s = 0
        self.cumulative_pnl = []
        for trade in trades:
            s += trade['pnl']
            self.cumulative_pnl.append(s)
