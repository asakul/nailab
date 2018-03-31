
from nailab.data.datasource import DataSource

import glob
import os

class CsvFolderDataSource(DataSource):

    def __init__(self, name, path):
        super().__init__(name)

        self.path = path
        self.feeds = []
        self._discover_feeds()

    def available_feeds(self):
        return self.feeds

    def get_feed(self, feed_id):
        pass

    def _discover_feeds(self):
        files = glob.glob(self.path + '/*.csv')
        self.feeds = [os.path.basename(f) for f in files]

