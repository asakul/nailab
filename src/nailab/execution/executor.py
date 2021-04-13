
import sys
import importlib
from importlib.machinery import SourceFileLoader
import inspect
from PyQt5 import QtCore

from naiback.strategy import Strategy

class Executor:

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
                strategy = klass()
                for feed in feeds:
                    strategy.add_feed(feed)

                (commission_percentage, commission_per_share) = self.load_commissions()

                strategy.broker.set_commission(commission_percentage, commission_per_share)
                if extents is None:
                    strategy.run()
                else:
                    strategy.run(from_time=extents[0], to_time=extents[1])

                results = strategy.get_analyzer('stats').get_result()
                trades = strategy.get_analyzer('tradeslist').get_result()
                equity = strategy.get_analyzer('equity').get_result()
                return (results, trades, equity)



    def load_commissions(self):
        s = QtCore.QSettings()

        return (float(s.value("commission/percentage", 0)), float(s.value("commission/per_share", 0)))
        
