# AutoModder

### .index's Unity APK Auto-Modder

## Setup
- [Python](https://www.python.org/)
- `pip install UnityPy`
- See [APK-Modding-Guide](https://github.com/twhlynch/APK-Modding-Guide) for requirements

## Usage

### Download apks

- install (QAutoDL)[https://github.com/twhlynch/QAutoDL]
- run `download_apks.py` (input example: `polarchase, gorilla sprinters, bad tag`)
- links will open in your browser and if you have the extension the apks will be downloaded

### Single APK mod

```usage: AutoModder.py [-h] [--noWalls] [--noGrav] [--pvp] apk_path```

### Bulk APK mod

- move APK files to this directory
- run `bulk_run.bat`
- APKs will be modded with `--noWalls`
