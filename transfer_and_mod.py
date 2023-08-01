import os, time, shutil, subprocess

def transfer_apks(list, folder):
    for name in list:
        if name.endswith(".apk"):
            print(f"Transferring {name}")
            file_path = os.path.join(folder, name)
            shutil.copy(file_path, name)
            os.remove(file_path)
            subprocess.Popen(["python", "AutoModder.py", name, "--noWalls"])

def scan_folder(folder):
    while True:
        files = os.listdir(folder)
        if files:
            transfer_apks(files, folder)
        time.sleep(5)

if __name__ == "__main__":
    scan_folder(os.path.join(os.path.expandvars("%USERPROFILE%"), "Downloads"))