@echo off

venv\Scripts\activate

:: Inicia os módulos Python
python ini.py

:: Debuga com o Flask
call flask run --debug
