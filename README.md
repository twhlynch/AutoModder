# AutoModder

### .index's Ultimate Unity APK Auto-Modder

## Setup
- [Python](https://www.python.org/)
- `pip install UnityPy`
- [Apktool](https://ibotpeaches.github.io/Apktool/) added to PATH
- [jarsigner (JDK)](https://www.oracle.com/java/technologies/downloads/) added to PATH
- [zipalign (Command-line tools)](https://developer.android.com/studio#command-line-tools-only) added to PATH

```usage: AutoModder.py [-h] [--noWalls] [--noGrav] [--pvp] apk_path```

## How it works
- Decompile APK with APKTool
- Open data.unity3d with UnityPy
- Enable and Disable required assets
- Save data.unity3d
- Recompile APK with APKTool
- Sign and ZipAlign
