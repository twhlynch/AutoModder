import UnityPy

noWalls = True
noGrav = True
pvp = True

enable = [ 'mod', 'admin', 'owner', 'menu', 'perm', 'access', 'vip', 'trust', 'support', 'artist' ]
disable = [ 'block', 'vent', 'door', 'restrict', 'barrier', 'security', 'protect', 'anti' ]
ignore = [ 'event', 'mode' ]
reenable = [ 'moder' ]
scale = [ '' ]

if noWalls:
    disable.append('wall')
if noGrav:
    enable.append('grav')
    scale.append('grav')
    reenable.append('grav')
if pvp:
    enable.append('pvp')
    scale.append('pvp')

env = UnityPy.load("data.unity3d")

for obj in env.objects:
    if obj.type.name == "GameObject":
        data = obj.read()

        was = data.m_IsActive
        will = "enable" if was else "disable"
        color = "\u001B[32m" if was else "\u001B[31m"
        changed = False

        for key in enable:
            if key in data.name.lower():
                data.m_IsActive = True
                changed = True
                will = "enable"

        for key in disable:
            if key in data.name.lower():
                data.m_IsActive = False
                changed = True
                will = "disable"

        for key in ignore:
            if key in data.name.lower():
                data.m_IsActive = was
                changed = True
                will = "enable" if was else "disable"

        for key in reenable:
            if key in data.name.lower():
                data.m_IsActive = True
                changed = True
                will = "enable"

        for key in scale:
            if key in data.name.lower():
                print(f"\u001B[34mScaling   {color}|\u001B[0m GameObject {data.name}")
                target_path = data.read_typetree()['m_Component'][0]['component']['m_PathID']
                for obj2 in env.objects:
                    data2 = obj2.read()
                    if hasattr(data2, 'path_id'):
                        if data2.path_id == target_path:
                            print(f"\u001B[34mFound Path{color}|\u001B[0m {data2.type.name} {data2.name}")
                            data2.__setattr__("m_LocalScale", data2.__getattribute__('m_LocalScale') * 100)
                            print(f"\u001B[34mScaled to {color}|\u001B[0m {data2.__getattribute__('m_LocalScale')}")
                            data2.save()
                            break

        if changed:
            if will == "enable" and was == False:
                print(f"\u001B[32mEnabled   {color}|\u001B[0m GameObject {data.name}")
            elif will == "disable" and was == True:
                print(f"\u001B[31mDisabled  {color}|\u001B[0m GameObject {data.name}")
            else:
                print(f"\u001B[33mIgnoring  {color}|\u001B[0m GameObject {data.name}")
        
        
        data.save()

env.save()

with open("data.unity3d", "wb") as f:
    f.write(env.file.save())