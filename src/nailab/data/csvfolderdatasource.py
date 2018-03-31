
from nailab.data.datasource import DataSource

from naiback.data.feeds.genericcsvfeed import GenericCSVFeed

import glob
import os

class CsvFolderDataSource(DataSource):

    def __init__(self, name, path):
        super().__init__(name)

        self.path = path
        self.feeds = []
        self._discover_feeds()

    def available_feeds(self):
        return [f[1] for f in self.feeds]

    def get_feed(self, feed_id):
        for path, f_id in self.feeds:
            if f_id == feed_id:
                with open(path, 'r') as f:
                    return GenericCSVFeed(f)
        raise NailabError('Unable to obtain feed: {}'.format(feed_id))


    def _discover_feeds(self):
        files = glob.glob(self.path + '/*.csv')
        self.feeds = [(f, os.path.basename(f)) for f in files]

