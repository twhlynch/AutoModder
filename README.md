# AutoModder

### .index's Unity APK Auto-Modder

## Setup
- [Python](https://www.python.org/)
- `pip install UnityPy`
- [Apktool](https://ibotpeaches.github.io/Apktool/) added to PATH
- Might need [JDK](https://www.oracle.com/java/technologies/downloads/) added to PATH
- [zipalign and Apksigner (Command-line tools)](https://developer.android.com/studio#command-line-tools-only) added to PATH
> For command line tools above: just download and use [these](https://github.com/twhlynch/Basic-APK-Modding-Guide/tree/main/bin/android_sdk)

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
