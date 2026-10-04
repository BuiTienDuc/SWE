@echo off
cd /d "%~dp0"
python evaluate.py --patch baseline
python evaluate.py --patch regression
python evaluate.py --patch partial
python evaluate.py --patch partial --expanded
python evaluate.py --patch fixed --expanded
pause
