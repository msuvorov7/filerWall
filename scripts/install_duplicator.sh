#!/bin/bash
cd ..
cp internal/pkg/duplicator/duplicator.py .
pyinstaller --onefile duplicator.py
sudo cp dist/duplicator /usr/local/bin

rm -rf dist build duplicator.spec duplicator.py
