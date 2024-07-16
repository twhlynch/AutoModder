# AutoModder

### .index's Unity APK Auto-Modder

## Setup
- [Python](https://www.python.org/) 3.12 or above
- See [APK-Modding-Guide](https://github.com/twhlynch/APK-Modding-Guide) for apktool, zipalign, and apksigner.
  
Run `python3 -m venv .` to initialize a python virtual environment
Run `bin/pip install UnityPy` to install UnityPy

If apktool, zipalign, and/or apksigner aren't added to your PATH, modify `binaries.json` with the paths to apktool, zipalign, and apksigner.
> Example: /Users/username/Library/Android/sdk/build-tools/34.0.0/zipalign

## Usage

### Single APK mod

```usage: bin/python AutoModder.py [-h] [--noWalls] [--noGrav] [--pvp] apk_path```

### Bulk APK mod

- move APK files to this directory
- run `bulk_run.bat`
- APKs will be modded with `--noWalls`

# Legal Disclaimer
Please be aware that using or distributing the output from this software may be against copyright legislation in your jurisdiction. You are responsible for ensuring that you're not breaking any laws.
