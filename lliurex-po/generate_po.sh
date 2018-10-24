#!/bin/bash

PYTHON_FILES="../install-files/usr/share/zero-server-wizard/master.py ../install-files/usr/share/zero-server-wizard/slave.py ../install-files/usr/share/zero-server-wizard/independent.py"
UI_FILES="../install-files/usr/share/zero-server-wizard/rsrc/main.glade"

cp $UI_FILES /tmp
mv /tmp/main.glade /tmp/main.ui

UI_FILES="/tmp/main.ui"

mkdir -p zero-server-wizard/

xgettext $UI_FILES $PYTHON_FILES -o zero-server-wizard/zero-server-wizard.pot

