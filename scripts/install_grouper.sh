#!/bin/bash
cd ..
cp internal/pkg/grouper/grouper.py .
pyinstaller --onefile grouper.py
sudo cp dist/grouper /usr/local/bin

rm -rf dist build grouper.spec grouper.py
