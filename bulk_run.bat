@echo off

for %%F in ("*.apk") do (
    start /B python AutoModder.py "%%F" --noWalls
)