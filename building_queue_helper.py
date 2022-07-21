current_buildings = {
    "Senat": 24,
    "Grotte": 0,
    "Scierie": 15,
    "Carriere": 15,
    "Mine d'argent": 12,
    "Marche": 3,
    "Port": 3,
    "Caserne": 5,
    "Remparts": 3,
    "Entrepot": 16,
    "Ferme": 36,
    "Academie": 24,
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


def auto_queue_builder():
    queue = []
    buildings = dict.copy(current_buildings)
    