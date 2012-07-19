#!/bin/bash
#
# Runs test.py through the patched pyinstaller, bundling everything into a single executable, then running it making sure it works
# As long as you don't see a traceback everything is groovy
#

cd pyinstaller
echo "Running  patched pyinstaller"
/usr/bin/python pyinstaller.py --PyObjC --onefile ../test.py
echo "Examining clipboard types with PyObjC bindings"
test/dist/test
#rm -rf test/
