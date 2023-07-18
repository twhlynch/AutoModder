import UnityPy, os, subprocess, argparse

def modUnity3d(path, noWalls, noGrav, pvp):
    enable = [ 'mod', 'admin', 'owner', 'menu', 'perm', 'access', 'vip', 'trust', 'support', 'artist' ]
    disable = [ 'block', 'vent', 'door', 'restrict', 'barrier', 'security', 'protect', 'anti' ]
    ignore = [ 'event', 'mode' ]
    reenable = [ 'moder' ]
    scale = [ ]

    if noWalls:
        disable.append('wall')
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

            for key in scale:
                if key in data.name.lower():
                    print(f"\u001B[34mScaling   {color}|\u001B[0m GameObject {data.name}")
                    target_path = tree['m_Component'][0]['component']['m_PathID']
                    for obj2 in env.objects:
                        data2 = obj2.read()
                        tree2 = data2.read_typetree()
                        if hasattr(data2, 'path_id'):
                            if data2.path_id == target_path:
                                print(f"\u001B[34mFound Path{color}|\u001B[0m {data2.type.name} {data2.name}")
                                tree2["m_LocalScale"] *= 100
                                print(f"\u001B[34mScaled to {color}|\u001B[0m {data2.__getattribute__('m_LocalScale')}")
                                obj2.save_typetree(tree2)
                                break

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
    print(f"Decompiling {apk_path} into {apk_path[:-4]}")
    sp = subprocess.Popen(["apktool", "d", "-f", apk_path], shell=True, stdin=subprocess.PIPE)
    sp.communicate(input=b'\n')

def recompile(apk_path):
    print(f"Recompiling {apk_path[:-4]} into {apk_path}")
    sp = subprocess.Popen(["apktool", "b", "-f", "-d", apk_path[:-4], "-o", f"tmp-{apk_path}"], shell=True, stdin=subprocess.PIPE)
    sp.communicate(input=b'\n')

    print(f"Signing {apk_path}")
    # Password is 123456
    sp = subprocess.Popen(["jarsigner", "-verbose", "-sigalg", "SHA1withRSA", "-digestalg", "SHA1", "-keystore", "index.keystore", f"tmp-{apk_path}", "index"], shell=True, stdin=subprocess.PIPE)
    sp.communicate(input=b'123456\n')

    print(f"Aligning {apk_path}")
    sp = subprocess.Popen(["zipalign", "-f", "-v", "4", f"tmp-{apk_path[:-4]}", f"modded-{apk_path}"], shell=True, stdin=subprocess.PIPE)
    sp.communicate(input=b'\n')

    print(f"Verifying {apk_path}")
    sp = subprocess.Popen(["jarsigner", "-verify", "-verbose", "-certs", f"modded-{apk_path}"], shell=True, stdin=subprocess.PIPE)
    sp.communicate(input=b'\n')

    os.remove(f"tmp-{apk_path}")

def main(apk_path, noWalls, noGrav, pvp):
    decompile(apk_path)
    apk_folder_path = apk_path[:-4]
    modUnity3d(f"{apk_folder_path}/assets/bin/Data/data.unity3d", noWalls, noGrav, pvp)
    recompile(apk_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("apk_path", help="Path to APK file")
    parser.add_argument("--noWalls", action="store_true", help="Disable walls")
    parser.add_argument("--noGrav", action="store_true", help="Disable gravity")
    parser.add_argument("--pvp", action="store_true", help="Enable PvP")
    args = parser.parse_args()

    print(args.apk_path, args.noWalls, args.noGrav, args.pvp)