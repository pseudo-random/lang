#!/bin/bash
python3 src/compiler_py/main.py src/compiler/main.txt > compile.js
node compile.js src/compiler/main.txt compile.js
node compile.js src/compiler/main.txt compile.js
