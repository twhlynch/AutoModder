import os, time, shutil, subprocess

def transfer_apks(list, processed, folder):
    for name in list:
        if name.endswith(".apk") and name not in processed:
            print(f"Transferring {name}")
            file_path = os.path.join(folder, name)
            shutil.copy(file_path, name)
            os.remove(file_path)
            subprocess.Popen(["python", "AutoModder.py", name, "--noWalls"])
            processed.append(name)

def scan_folder(folder):
    processed = []
    while True:
        files = os.listdir(folder)
        if files:
            transfer_apks(files, processed, folder)
        time.sleep(5)

if __name__ == "__main__":
    scan_folder(os.path.join(os.path.expandvars("%USERPROFILE%"), "Downloads"))