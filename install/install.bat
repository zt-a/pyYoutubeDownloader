@echo off
cd ../
python -m venv venv
cd venv/Scripts
activate.bat
cd ../..
pip install -r requirement.txt
