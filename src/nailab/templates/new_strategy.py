
new_strategy_template = '''
from naiback.strategy import Strategy

class MyStrategy(Strategy):

    def __init__(self):
        super().__init__()

    def execute(self):
        for i in self.bars.index[200:]:
            if self.last_position_is_active():
                pass
            else:
                pass
'''
