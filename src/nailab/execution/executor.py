
from importlib.machinery import SourceFileLoader
import inspect

from naiback.strategy import Strategy

class Executor:

    def __init__(self):
        pass

    def execute_from_file(self, path, feeds, extents=None):
        loader = SourceFileLoader('execution._current_strategy', path)
        mod = loader.load_module()
        for item in inspect.getmembers(mod, inspect.isclass):
            klass = item[1]
            if klass is not Strategy and issubclass(klass, Strategy):
                strategy = klass()
                for feed in feeds:
                    strategy.add_feed(feed)

                if extents is None:
                    strategy.run()
                else:
                    strategy.run(from_time=extents[0], to_time=extents[1])

                results = strategy.get_analyzer('stats').get_result()
                trades = strategy.get_analyzer('tradeslist').get_result()
                return (results, trades)


