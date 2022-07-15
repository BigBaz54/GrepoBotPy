current_buildings = {
    "Senat": 8,
    "Grotte": 0,
    "Scierie": 5,
    "Carriere": 5,
    "Mine d'argent": 5,
    "Marche": 3,
    "Port": 0,
    "Caserne": 5,
    "Remparts": 1,
    "Entrepot": 7,
    "Ferme": 6,
    "Academie": 3,
    "Temple": 3,
}

def queue_builder():
    queue = []
    entree = ""
    buildings = dict.copy(current_buildings)
    while entree != 'stop':
        print('Bâtiment à améliorer ?')
        entree = input()
        if entree in list(raccourcis):
            bat = raccourcis[entree]
            if bat != 'down':
                former_buildings = dict.copy(buildings)
                queue.append(bat)
                buildings[bat]+= 1
            else:
                buildings = dict.copy(former_buildings)
                queue.pop()
        else:
            print("mauvais input")
        print_dict(buildings)
        print(queue)
        print("\n\n\n\n\n\n\n\n\n")
    return queue

def print_dict(d):
    for e in list(d):
        print(e+": "+str(d[e]))



raccourcis = {
    "sen": "Senat",
    "gro": "Grotte",
    "sci": "Scierie",
    "car": "Carriere",
    "min": "Mine d'argent",
    "mar": "Marche",
    "por": "Port",
    "cas": "Caserne",
    "rem": "Remparts",
    "ent": "Entrepot",
    "fer": "Ferme",
    "aca": "Academie",
    "tem": "Temple",
    "down": "down"
}
