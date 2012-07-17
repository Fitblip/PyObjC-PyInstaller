#!/bin/bash

cd pyinstaller
echo "Running  patched pyinstaller"
/usr/bin/python pyinstaller.py --PyObjC --onefile ../test.py
echo "Examining clipboard types with PyObjC bindings"
test/dist/test
rm -rf test/
