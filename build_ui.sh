#!/bin/bash

/usr/bin/pyuic5 ui/csvdatasourceconfigwidget.ui > src/nailab/ui_gen/csvdatasourceconfigwidget.py
/usr/bin/pyuic5 ui/equitychartwidget.ui > src/nailab/ui_gen/equitychartwidget.py
/usr/bin/pyuic5 ui/mainwindow.ui > src/nailab/ui_gen/mainwindow.py
/usr/bin/pyuic5 ui/newdatasourcedialog.ui > src/nailab/ui_gen/newdatasourcedialog.py
/usr/bin/pyuic5 ui/strategywidget.ui > src/nailab/ui_gen/strategywidget.py
/usr/bin/pyuic5 ui/tradeslistwidget.ui > src/nailab/ui_gen/tradeslistwidget.py
/usr/bin/pyuic5 ui/performancewidget.ui > src/nailab/ui_gen/performancewidget.py

/usr/bin/pyrcc5 nailab.qrc -o src/nailab/nailab_rc.py


