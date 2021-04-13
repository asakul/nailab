#!/bin/bash

pyuic5 ui/csvdatasourceconfigwidget.ui > src/nailab/ui_gen/csvdatasourceconfigwidget.py
pyuic5 ui/equitychartwidget.ui > src/nailab/ui_gen/equitychartwidget.py
pyuic5 ui/mainwindow.ui > src/nailab/ui_gen/mainwindow.py
pyuic5 ui/newdatasourcedialog.ui > src/nailab/ui_gen/newdatasourcedialog.py
pyuic5 ui/strategywidget.ui > src/nailab/ui_gen/strategywidget.py
pyuic5 ui/tradeslistwidget.ui > src/nailab/ui_gen/tradeslistwidget.py
pyuic5 ui/performancewidget.ui > src/nailab/ui_gen/performancewidget.py
pyuic5 ui/settingswindow.ui > src/nailab/ui_gen/settingswindow.py
pyuic5 ui/statisticwidget.ui > src/nailab/ui_gen/statisticwidget.py

pyrcc5 nailab.qrc -o src/nailab/nailab_rc.py


