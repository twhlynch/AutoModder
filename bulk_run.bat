@echo off

for %%F in ("*.apk") do (
    start /B bin/python AutoModder.py "%%F" --noWalls
)