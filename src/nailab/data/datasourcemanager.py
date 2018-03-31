
from nailab.data.csvfolderdatasource import CsvFolderDataSource

class DataSourceManager:

    def __init__(self):
        self.sources = []

    def save_sources(self):
        pass

    def load_sources(self):
        self.add_source(CsvFolderDataSource('default', '/tmp'))

    def add_source(self, source):
        self.sources.append(source)

    def all_sources(self):
        return self.sources[:]

