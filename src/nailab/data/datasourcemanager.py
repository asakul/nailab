
from data.csvfolderdatasource import CsvFolderDataSource

class DataSourceManager:

    def __init__(self):
        self.sources = []

    def save_sources(self, settings):
        serialized = []
        for source in self.sources:
            serialized.append((source.type, source.serialize()))
        settings.setValue("data_sources", serialized)

    def load_sources(self, settings):
        self.sources = []
        serialized = settings.value("data_sources")
        if serialized is not None:
            for s in serialized:
                if s[0] == "csv":
                    self.add_source(CsvFolderDataSource.deserialize(s[1]))

    def add_source(self, source):
        self.sources.append(source)

    def get_source(self, name):
        for source in self.sources:
            if source.name == name:
                return source
        return None

    def remove_source(self, name):
        for source in self.sources:
            if source.name == name:
                self.sources.remove(source)
                return

    def all_sources(self):
        return self.sources[:]

