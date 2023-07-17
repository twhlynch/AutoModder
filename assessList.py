import UnityPy

noWalls = True
noGrav = True
pvp = True

enable = [ 'mod', 'admin', 'owner', 'menu', 'perm', 'access', 'vip', 'trust', 'support', 'artist' ]
disable = [ 'block', 'vent', 'door', 'restrict', 'barrier', 'security', 'protect', 'anti' ]
no_disable = [ 'event', 'mode' ]
scale = []

if noWalls:
    disable.append('wall')
if noGrav:
    enable.append('grav')
    scale.append('grav')
if pvp:
    enable.append('pvp')
    scale.append('pvp')

env = UnityPy.load("data.unity3d")

for obj in env.objects:
    if obj.type.name == "GameObject":
        data = obj.read()

        state = data.m_IsActive
        color = "\u001B[32m" if state else "\u001B[31m"
        ignore = False

        for key in enable:
            if key in data.name.lower():
                if 'mode' not in data.name.lower():
                    print(f"\u001B[32mEnabling  {color}|\u001B[0m GameObject {data.name}")
                    data.m_IsActive = True
                else:
                    ignore = True

        for key in disable:
            if key in data.name.lower():
                if 'event' not in data.name.lower():
                    print(f"\u001B[31mDisabling {color}|\u001B[0m GameObject {data.name}")
                    data.m_IsActive = False
                else:
                    ignore = True

        for key in scale:
            if key in data.name.lower():
                print(f"\u001B[34mScaling {color}|\u001B[0m GameObject {data.name}...")
                target_path = data.read_typetree()['m_Component'][0]['component']['m_PathID']
                for obj2 in env.objects:
                    data2 = obj2.read()
                    if data2.path_id == target_path:
                        data2.__setattr__("m_LocalScale", data2.__getattribute__('m_LocalScale') * 100)
                        data2.save()

        if ignore:
            print(f"\u001B[33mIgnoring  {color}|\u001B[0m GameObject {data.name}")
        
        data.save()

env.save()

with open("data.unity3d", "wb") as f:
    f.write(env.file.save())