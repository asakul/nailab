

import sys
import importlib
from importlib.machinery import SourceFileLoader
import inspect

from naiback.strategy import Strategy

import numpy as np
import math

def render_float(a):
    return "{:.3f}".format(a)


def render_ratio(a, b):
    if b != 0:
        return a / b
    else:
        return 0

class PortfolioExecutor:

    def __init__(self):
        pass

    def execute_from_file(self, path, feeds, extents=None):
        if "execution._current_strategy" in sys.modules:
            del sys.modules["execution._current_strategy"]
        loader = SourceFileLoader('execution._current_strategy', path)
        mod = loader.load_module()
        for item in inspect.getmembers(mod, inspect.isclass):
            klass = item[1]
            if klass is not Strategy and issubclass(klass, Strategy):
                all_trades = []
                for feed in feeds:
                    strategy = klass()
                    strategy.add_feed(feed)

                    if extents is None:
                        strategy.run()
                    else:
                        strategy.run(from_time=extents[0], to_time=extents[1])

                    trades = strategy.get_analyzer('tradeslist').get_result()
                    all_trades = self.merge_trades(all_trades, trades)

                results = self.calc_stats(all_trades)
                equity = self.calc_equity(all_trades)
                return (results, all_trades, equity)

    def merge_trades(self, trades1, trades2):
        all_trades = list(sorted(trades1 + trades2, key=lambda x: x['entry_time']))
        result = []
        current_trades = []
        max_trades = 3
        for trade in all_trades:
            if len(current_trades) < max_trades:
                current_trades.append(trade)
                result.append(trade)
            new_current_trades = []
            for ct in current_trades:
                if ct['exit_time'] < trade['entry_time']:
                    new_current_trades.append(ct)
                else:
                    # possibly adjust the balance
                    pass
            current_trades = new_current_trades
        return result
                    
    def calc_stats(self, trades):
        longs = list(filter(lambda x: x['is_long'], trades))
        shorts = list(filter(lambda x: not x['is_long'], trades))

        result = { 'all' : {}, 'long' : {}, 'short' : {} }
        result['all']['net_profit'] = sum([t['pnl'] for t in trades])
        result['long']['net_profit'] = sum([t['pnl'] for t in longs])
        result['short']['net_profit'] = sum([t['pnl'] for t in shorts])

        result['all']['bars_in_trade'] = 0 # TODO?
        result['long']['bars_in_trade'] = 0
        result['short']['bars_in_trade'] = 0

        result['all']['profit_per_bar'] = 0
        result['long']['profit_per_bar'] = 0
        result['short']['profit_per_bar'] = 0

        result['all']['number_of_trades'] = len(trades)
        result['long']['number_of_trades'] = len(longs)
        result['short']['number_of_trades'] = len(shorts)

        result['all']['avg'] = render_ratio(result['all']['net_profit'], result['all']['number_of_trades'])
        result['long']['avg'] = render_ratio(result['long']['net_profit'], result['long']['number_of_trades'])
        result['short']['avg'] = render_ratio(result['short']['net_profit'], result['short']['number_of_trades'])

        result['all']['avg_percentage'] = render_ratio(sum([t['profit_percentage'] for t in trades]), result['all']['number_of_trades'])
        result['long']['avg_percentage'] = render_ratio(sum([t['profit_percentage'] for t in longs]), result['long']['number_of_trades'])
        result['short']['avg_percentage'] = render_ratio(sum([t['profit_percentage'] for t in shorts]), result['short']['number_of_trades'])

        result['all']['avg_bars'] = render_ratio(result['all']['bars_in_trade'], result['all']['number_of_trades'])
        result['long']['avg_bars'] = render_ratio(result['long']['bars_in_trade'], result['long']['number_of_trades'])
        result['short']['avg_bars'] = render_ratio(result['short']['bars_in_trade'], result['short']['number_of_trades'])

        result['all']['won'] = len(list(filter(lambda t: t['pnl'] > 0, trades)))
        result['long']['won'] = len(list(filter(lambda t: t['pnl'] > 0, longs)))
        result['short']['won'] = len(list(filter(lambda t: t['pnl'] > 0, shorts)))

        result['all']['lost'] = len(list(filter(lambda t: t['pnl'] <= 0, trades)))
        result['long']['lost'] = len(list(filter(lambda t: t['pnl'] <= 0, longs)))
        result['short']['lost'] = len(list(filter(lambda t: t['pnl'] <= 0, shorts)))

        result['all']['total_won'] = sum(map(lambda t: t['pnl'], filter(lambda t: t['pnl'] > 0, trades)))
        result['long']['total_won'] = sum(map(lambda t: t['pnl'], filter(lambda t: t['pnl'] > 0, longs)))
        result['short']['total_won'] = sum(map(lambda t: t['pnl'], filter(lambda t: t['pnl'] > 0, shorts)))

        result['all']['total_lost'] = sum(map(lambda t: t['pnl'], filter(lambda t: t['pnl'] <= 0, trades)))
        result['long']['total_lost'] = sum(map(lambda t: t['pnl'], filter(lambda t: t['pnl'] <= 0, longs)))
        result['short']['total_lost'] = sum(map(lambda t: t['pnl'], filter(lambda t: t['pnl'] <= 0, shorts)))

        result['all']['profit_factor'] = render_ratio(result['all']['total_won'], -result['all']['total_lost'])
        result['long']['profit_factor'] = render_ratio(result['long']['total_won'], -result['long']['total_lost'])
        result['short']['profit_factor'] = render_ratio(result['short']['total_won'], -result['short']['total_lost'])

        mean = np.mean(list(map(lambda x: x['pnl'], trades)))
        stddev = np.std(list(map(lambda x: x['pnl'], trades)))
        sharpe = mean / stddev
        tstat = sharpe * math.sqrt(len(trades))
        result['all']['sharpe_ratio'] = sharpe
        result['all']['t_stat'] = tstat

        mean = np.mean(list(map(lambda x: x['pnl'], longs)))
        stddev = np.std(list(map(lambda x: x['pnl'], longs)))
        sharpe = mean / stddev
        tstat = sharpe * math.sqrt(len(longs))
        result['long']['sharpe_ratio'] = sharpe
        result['long']['t_stat'] = tstat

        mean = np.mean(list(map(lambda x: x['pnl'], shorts)))
        stddev = np.std(list(map(lambda x: x['pnl'], shorts)))
        sharpe = mean / stddev
        tstat = sharpe * math.sqrt(len(shorts))
        result['short']['sharpe_ratio'] = sharpe
        result['short']['t_stat'] = tstat

        return result

    def calc_equity(self, trades):
        sorted_trades = sorted(trades, key=lambda x: x['exit_time'])
        equity = []
        current = 0
        for t in sorted_trades:
            current += t['pnl']
            equity.append(current)

