import UnityPy, os, subprocess, argparse, shutil, json

with open("binaries.json", "r") as f:
    binaries = json.load(f)
zipalign = binaries["zipalign"]
apktool = binaries["apktool"]
apksigner = binaries["apksigner"]

def modUnity3d(path, noWalls, noGrav, pvp):
    enable = []
    disable = []
    ignore = []
    reenable = []
    scale = []
    enable_is = []
    ends_in = []
    disable_is = []
    
    with open("config.json", "r") as f:
        config = json.load(f)
        
    if config["enable"]:
        enable.extend(config["enable"])
    if config["disable"]:
        disable.extend(config["disable"])
    if config["ignore"]:
        ignore.extend(config["ignore"])
    if config["reenable"]:
        reenable.extend(config["reenable"])
    if config["scale"]:
        scale.extend(config["scale"])
    if config["enable_is"]:
        enable_is.extend(config["enable_is"])
    if config["ends_in"]:
        ends_in.extend(config["ends_in"])
    if config["disable_is"]:
        disable_is.extend(config["disable_is"])

    if noWalls:
        disable.append('wall')
        disable.append('roof')
    if noGrav:
        enable.append('grav')
        scale.append('grav')
        reenable.append('grav')
    if pvp:
        enable.append('pvp')
        scale.append('pvp')

    env = UnityPy.load(path)

    for obj in env.objects:
        if obj.type.name == "GameObject":
            data = obj.read()
            tree = data.read_typetree()

            was = data.m_IsActive
            will = "enable" if was else "disable"
            color = "\u001B[32m" if was else "\u001B[31m"
            changed = False

            for key in enable:
                if key in data.name.lower():
                    tree["m_IsActive"] = True
                    changed = True
                    will = "enable"
                    
            for key in ends_in:
                if data.name.lower().endswith(key):
                    tree["m_IsActive"] = True
                    changed = True
                    will = "enable"

            for key in disable:
                if key in data.name.lower():
                    tree["m_IsActive"] = False
                    changed = True
                    will = "disable"

            for key in ignore:
                if key in data.name.lower():
                    tree["m_IsActive"] = was
                    changed = True
                    will = "enable" if was else "disable"

            for key in reenable:
                if key in data.name.lower():
                    tree["m_IsActive"] = True
                    changed = True
                    will = "enable"
                    
            for key in enable_is:
                if key == data.name.lower():
                    tree["m_IsActive"] = True
                    changed = True
                    will = "enable"
                    
            for key in disable_is:
                if key == data.name.lower():
                    tree["m_IsActive"] = False
                    changed = True
                    will = "disable"
                    
            for key in scale:
                if key in data.name.lower():
                    print(f"\u001B[34mScaling   {color}|\u001B[0m GameObject {data.name}")
                    transform = data.m_Transform.get_obj()
                    transform_tree = transform.read_typetree()
                    transform_tree["m_LocalScale"]["x"] *= 100
                    transform_tree["m_LocalScale"]["y"] *= 100
                    transform_tree["m_LocalScale"]["z"] *= 100
                    print(f'\u001B[34mScaled    {color}|\u001B[0m {data.name} to {transform_tree["m_LocalScale"]}')
                    transform.save_typetree(transform_tree)

            if changed:
                if will == "enable" and was == False:
                    print(f"\u001B[32mEnabled   {color}|\u001B[0m GameObject {data.name}")
                elif will == "disable" and was == True:
                    print(f"\u001B[31mDisabled  {color}|\u001B[0m GameObject {data.name}")
                else:
                    print(f"\u001B[33mIgnoring  {color}|\u001B[0m GameObject {data.name}")
            
            obj.save_typetree(tree)

    with open(path, "wb") as f:
        f.write(env.file.save())

def decompile(apk_path):
    print(f"\u001B[32mDecompiling {apk_path} into {apk_path[:-4]}\u001B[0m")
    sp = subprocess.Popen(f"{apktool} d -f {apk_path} -o {apk_path[:-4]}", shell=True, stdin=subprocess.PIPE)
    sp.communicate(input=b'\n')

def recompile(apk_path):
    print(f"\u001B[32mRecompiling {apk_path[:-4]} into {apk_path}\u001B[0m")
    sp = subprocess.Popen(f"{apktool} b -f --use-aapt2 -d {apk_path[:-4]} -o tmp-{apk_path}", shell=True, stdin=subprocess.PIPE)
    sp.communicate(input=b'\n')

    print(f"\u001B[32mAligning {apk_path}\u001B[0m")
    sp = subprocess.Popen(f"{zipalign} -p 4 tmp-{apk_path} tmp2-{apk_path}", shell=True, stdin=subprocess.PIPE)
    sp.communicate(input=b'\n')

    print(f"\u001B[32mSigning {apk_path}\u001B[0m")
    sp = subprocess.Popen(f"{apksigner} sign --key index.pk8 --cert index.pem --v4-signing-enabled false --out modded-{apk_path} tmp2-{apk_path}", shell=True, stdin=subprocess.PIPE)
    sp.communicate(input=b'\n')

def main(apk_path, noWalls, noGrav, pvp):
    # if not os.path.exists(apk_path[:-4]):
    #     os.mkdir(f"{apk_path[:-4]}")
    # open(f"tmp-{apk_path}", 'a').close()
    # open(f"tmp2-{apk_path}", 'a').close()
    # open(f"modded-{apk_path}", 'a').close()
    
    decompile(apk_path)
    apk_folder_path = apk_path[:-4]
    modUnity3d(f"{apk_folder_path}/assets/bin/Data/data.unity3d", noWalls, noGrav, pvp)
    recompile(apk_path)

    os.remove(f"tmp-{apk_path}")
    os.remove(f"tmp2-{apk_path}")
    shutil.rmtree(f"{apk_path[:-4]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("apk_path", help="Path to APK file")
    parser.add_argument("--noWalls", action="store_true", help="Disable walls")
    parser.add_argument("--noGrav", action="store_true", help="Disable gravity")
    parser.add_argument("--pvp", action="store_true", help="Enable PvP")
    args = parser.parse_args()

    main(args.apk_path, args.noWalls, args.noGrav, args.pvp)