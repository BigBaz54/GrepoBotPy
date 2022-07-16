from lib2to3.pgen2 import driver
from math import floor
from random import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from termcolor import colored
from datetime import datetime
from ast import literal_eval


def action_selector():
    connect()
    close_daily_reward()
    if (auto_attack_enabled):
            # print(actions_current_town[i]['name'] + ' est activé !')
            if (is_ready_auto_attack()):
                # print(actions_current_town[i]['name'] + ' est prêt !')
                do_auto_attack()
                return
    if (auto_farm_towns_enabled):
            # print(actions_current_town[i]['name'] + ' est activé !')
            if (is_ready_auto_farm_towns()):
                # print(actions_current_town[i]['name'] + ' est prêt !')
                do_auto_farm_towns()
                return
    actions_current_town = actions[get_current_city_name()]
    print_with_time_and_color('\nJe sélectionne une action à effectuer dans la ville : ' +
                            get_current_city_name(), 'red')
    for i in range(len(actions_current_town.keys())):
        if (actions_current_town[i]['activated']):
            # print(actions_current_town[i]['name'] + ' est activé !')
            if not (actions_current_town[i]['is_stacked_function']()):
                if (actions_current_town[i]['is_ready_function']()):
                    # print(actions_current_town[i]['name'] + ' est prêt !')
                    actions_current_town[i]['do_function']()
                    return
                else:
                    print(actions_current_town[i]['name']+" n'est pas stacked")
                    switch_town()
                    if(get_current_city_name() == '1. Ville 1'):
                        print('Toutes les villes ont été parcourues')
                        do_auto_festival()
                        do_auto_triumph()
                        sleep(sleep_time_randomizer(60, 10))
                    return
    print("Cette ville est full stacked !!")
    switch_town()
    if(get_current_city_name() == '1. Ville 1'):
        print('Toutes les villes ont été parcourues')
        do_auto_festival()
        do_auto_triumph()
        sleep(sleep_time_randomizer(60, 10))


def try_action_selector():
    try:
        action_selector()
    except KeyboardInterrupt:
        build = open("setup_to_edit/building_queues.txt", "w")
        build.write(str(building_queues))
        build.close()
        raise
    except Exception:
        print_with_time_and_color(
            '\n\nERREUR !! vas-y je retente OKLM\n\n', 'red')
        try:
            get_element(".close_all").click()
            short_pause()
        except Exception:
            sleep(0.001)
        try_action_selector()


def connect():
    if driver.current_url in ['https://fr.grepolis.com/']:
        usr = driver.find_elements(By.ID, 'login_userid')[0]
        usr.send_keys(USERNAME)
        pwd = driver.find_elements(By.ID, 'login_password')[0]
        pwd.send_keys(PASSWORD)
        pwd.send_keys(Keys.ENTER)
        sleep(10)
        driver.find_elements(By.CSS_SELECTOR, 'li.world_name')[0].click()
        print_with_time_and_color('\nJe suis connecté !', 'green')
        long_pause()
    if driver.current_url in ['https://fr0.grepolis.com/start?nosession']:
        sleep(10)
        driver.find_elements(By.CSS_SELECTOR, 'li.world_name')[0].click()
        print_with_time_and_color('\nJe suis connecté !', 'green')
        long_pause()


def switch_town():
    print_with_time_and_color('\n\n--Passage à la ville suivante--', 'magenta')
    get_element('.btn_next_town').click()

# switch to the town whose id (int) is given
def switch_to_town_by_id(city_id):
    driver.execute_script("TownSwitch.prototype.townSwitch(" + str(city_id) +")")



##################################
########## view_functions ########
##################################

def close_all_windows():
    print('Fermeture des fenêtres')
    driver.execute_script("GPWindowMgr.closeAll()")
    short_pause()


def open_city_overview():
    print("Affichage de l'aperçu de la ville")
    driver.execute_script("document.getElementsByClassName('city_overview')[0].click()")
    short_pause()


def open_map():
    print("Affichage de la carte")
    driver.execute_script("document.getElementsByClassName('island_view')[0].click()")
    short_pause()


def open_main():
    print("Affichage du sénat")
    driver.execute_script("MainWindowFactory.openMainWindow()")
    short_pause()


def open_place():
    print("Affichage de l'agora")
    driver.execute_script("PlaceWindowFactory.openPlaceWindow()")
    short_pause()


def open_hide():
    print("Affichage de la grotte")
    driver.execute_script("HideWindowFactory.openHideWindow()")
    short_pause()


def open_docks():
    print("Affichage du port")
    driver.execute_script("DocksWindowFactory.openDocksWindow()")
    short_pause()


def open_market():
    print("Affichage du marché")
    driver.execute_script("MarketWindowFactory.openMarketWindow()")
    short_pause()


def open_academy():
    print("Affichage de l'académie")
    driver.execute_script("AcademyWindowFactory.openAcademyWindow()")
    short_pause()


def open_barracks():
    print("Affichage de la caserne")
    driver.execute_script("BarracksWindowFactory.openBarracksWindow()")
    short_pause()


def open_farm_town_overview():
    print("Affichage de l'aperçu des VP")
    driver.execute_script("FarmTownOverviewWindowFactory.openFarmTownOverview()")
    short_pause()


def open_culture_overview():
    print("Affichage de l'aperçu de la Culture")
    driver.execute_script("TownOverviewWindowFactory.openCultureOverview()")
    short_pause()


def open_attack_planer():
    print("Affichage du planificateur")
    driver.execute_script("AttackPlannerWindowFactory.openAttackPlannerWindow()")
    short_pause()


def close_daily_reward():
    if datetime.now().strftime('%H') == '23' and int(datetime.now().strftime('%M')) >= 58:
        print_with_time_and_color("\nEn attente du bonus quotidien", 'red')
        while int(datetime.now().strftime('%M')) != 0:
            sleep(10)
        open_main()
        sleep(3)
        close_all_windows()


def close_front_window():
    print("Fermeture de la fenêtre")
    driver.execute_script("WM.closeFrontWindow()")
    short_pause()




##################################
########## get_functions #########
##################################

def get_current_city_building_queue_length():
    length = driver.execute_script('return ITowns.getCurrentTown().buildingOrders().length')
    return length


def get_current_city_resources():
    return driver.execute_script('return ITowns.getCurrentTown().resources()')


def get_current_city_wood():
    return get_current_city_resources()['wood']


def get_current_city_stone():
    return get_current_city_resources()['stone']


def get_current_city_iron():
    return get_current_city_resources()['iron']


def get_current_city_favor():
    return driver.execute_script('return ITowns.getCurrentTown().resources().favor')


def get_current_city_name():
    return get_element(".town_name").get_attribute('innerText')


def get_current_city_storage():
    return driver.execute_script('return ITowns.getCurrentTown().getStorage()')


def get_current_city_pop():
    return driver.execute_script('return ITowns.getCurrentTown().getAvailablePopulation()')


def get_current_city_trade_capacity():
    return driver.execute_script('return ITowns.getCurrentTown().getAvailableTradeCapacity()')

# returns a dictionary with the names of all the land units of this God as the keys and the number of units as the values
def get_current_city_land_units():
    return driver.execute_script('return ITowns.getCurrentTown().getLandUnits()')

# return a dictionary with the name of all the researches as keys and True or False as the values
# be careful : the dict contains 'id': <a number>
def get_current_city_researches():
    return driver.execute_script('return ITowns.getCurrentTown().getResearches().attributes')

# returns a list of strings representing the names of the researches unlocked at the current academy lvl
def get_current_city_unlocked_researches():
    open_academy()
    res = driver.execute_script("res = [];document.querySelectorAll('.column.active>.research_box>.research_icon').forEach((e) => {res.push(e.className.split(' ')[2])}); return res")
    close_front_window()
    return res


def get_current_city_researching_queue_length():
    open_academy()
    l = driver.execute_script("document.querySelectorAll('.queued_building_order').length")
    close_front_window()
    return l if (l!=None) else 0

# returns a list of strings representing the names of the available researches
def get_current_city_available_researches():
    open_academy()
    res = driver.execute_script("res = [];document.querySelectorAll('.column.active>.research_box>.btn_upgrade').forEach((e) => {res.push(e.dataset['research_id'])}); return res")
    close_front_window()
    return res

# returns a string of the name of the next research to do, or None if no needed research is available
def get_current_city_next_research():
    r = get_current_city_available_researches()
    for e in researches_to_get[get_current_city_name()]:
        if e in r:
            return e

# returns a dictionary with the names of the units in the city as keys and the number of units as the values
# contains land and naval units
def get_current_city_units():
    return driver.execute_script('return ITowns.getCurrentTown().units()')

# returns an int representing the length of the recruiting queue (barracks + docks)
def get_current_city_recruiting_queue_length():
    return driver.execute_script('return ITowns.getCurrentTown().getUnitOrdersCollection().length')

# returns the id (int) of the current city
def get_current_city_id():
    return driver.execute_script("return ITowns.getCurrentTown().id")


# returns a list of strings containing the names of all the naval units
def get_naval_units_list():
    return ['big_transporter', 'bireme', 'attack_ship', 'demolition_ship', 'small_transporter', 'trireme', 'colonize_ship', 'sea_monster', 'siren']

# returns a tuple containing :
# - a list of dict containing the series of orders possible to send in the city
# that uses the most free pop and according to the city goal army :
# [{'unit': <name>, 'amount': <amount>}, {'unit': <name>, 'amount': <amount>}, ... ]
# (only takes units whose research is done)
# - the pop used by these orders
def get_current_city_next_recruiting_order():
    # only takes those whose research is done
    goal_army = goal_armies[get_current_city_name()]
    goal_army_researched = [e for e in goal_army if (get_current_city_researches()[e['unit']])]
    n = len(goal_army_researched)
    rounding_scopes = []
    current_army = get_current_city_units()
    left_needed_army_researched = [{'unit': goal_army_researched[i]['unit'], 'amount': goal_army_researched[i]['amount']-(current_army[goal_army_researched[i]['unit']] if (goal_army_researched[i]['unit'] in list(current_army)) else 0 )} for i in range(n)]
    for e in left_needed_army_researched:
        rounding_scope = floor((e['amount']/30))+1
        e['amount']=e['amount']-e['amount']%rounding_scope
        rounding_scopes.append(rounding_scope)
    wood = get_current_city_wood()
    stone = get_current_city_stone()
    iron = get_current_city_iron()
    pop = get_current_city_pop()
    favor = get_current_city_favor()
    tested_comp = [0]*n
    best_pop_cost = 0
    while(tested_comp != [e['amount'] for e in left_needed_army_researched]):
        tested_comp[-1]+=rounding_scopes[-1]
        for i in range(n-1, -1, -1):
            if tested_comp[i] > left_needed_army_researched[i]['amount']:
                tested_comp[i]=0
                tested_comp[i-1]+=rounding_scopes[i-1]
        # traitement
        wood_cost = 0
        stone_cost = 0
        iron_cost = 0
        pop_cost = 0
        favor_cost = 0
        for i in range(n):
            wood_cost += units[goal_army_researched[i]['unit']]['resources']['wood']*tested_comp[i]
            stone_cost += units[goal_army_researched[i]['unit']]['resources']['stone']*tested_comp[i]
            iron_cost += units[goal_army_researched[i]['unit']]['resources']['iron']*tested_comp[i]
            pop_cost += units[goal_army_researched[i]['unit']]['population']*tested_comp[i]
            favor_cost += units[goal_army_researched[i]['unit']]['favor']*tested_comp[i]
        
        if (wood_cost<=wood) and (stone_cost<=stone) and (iron_cost<=iron) and (pop_cost<=pop) and (favor_cost<=favor):
            # print(tested_comp)
            # print("w", wood_cost, "s", stone_cost, "i", iron_cost, "p", pop_cost, "f", favor_cost, "\n")
            if (pop_cost>best_pop_cost):
                best_pop_cost = pop_cost
                best_tested_comp = list.copy(tested_comp)
                # print(best_tested_comp)
        else: 
            for i in range(1, n+1):
                if tested_comp[i:] == [0]*(n-i):
                    for j in range(i,n):
                        tested_comp[j]=left_needed_army_researched[j]['amount']
    next_order = [{'unit': goal_army_researched[i]['unit'], 'amount': best_tested_comp[i]} for i in range(n) if best_tested_comp[i]!=0]
    return next_order, best_pop_cost




##################################
########## do_functions ##########
##################################

def do_auto_attack():
    connect()
    print_with_time_and_color('\n--do_auto_attack--', 'blue')
    print('Sauvegarde de la ville courante')
    city_id = get_current_city_id()
    open_attack_planer()
    print('Affichage du plan courant')
    get_element('td.ap_name>a').click()
    short_pause()
    print('Tri des attaques par départ croissant')
    get_element('.send_at').click()
    short_pause()
    row = get_element('ul.attacks_list>li>.row3').get_attribute('innerText')
    t = row[-8:]
    h = int(t[:2])
    m = int(t[3:5])
    s = int(t[6:8])
    print('Préparation de la prochaine attaque')
    get_element('ul.attacks_list>li>.attack_icon').click()
    short_pause()
    atk_btn = get_element('#btn_attack_town')
    while int(datetime.now().strftime('%H'))!= h:
        sleep(0.1)
    while int(datetime.now().strftime('%M'))!= m:
        sleep(0.1)
    while int(datetime.now().strftime('%S'))<= (s-1):
        sleep(0.001)
    atk_btn.click()
    print_with_time_and_color('Attaque lancée !')
    short_pause()
    close_all_windows()
    print("Retour sur la ville courante")
    switch_to_town_by_id(city_id)
    short_pause()
    open_attack_planer()
    print('Affichage du plan courant')
    get_element('td.ap_name>a').click()
    short_pause()
    print('Tri des attaques par départ croissant')
    get_element('.send_at').click()
    short_pause()
    print("Suppression de l'attaque lancée")
    get_element('.btn_remove_attack').click()
    short_pause()
    close_all_windows()


def do_auto_build():
    connect()
    print_with_time_and_color('\n--do_auto_build--', 'blue')
    # open_city_overview()
    open_main()
    print("Lancement de la construction")
    get_element(
        building_buttons_queries[building_queues[get_current_city_name()][0]]).click()
    building_queues[get_current_city_name(
    )] = building_queues[get_current_city_name()][1:]
    print("Nouvelle file de construction : ",
        building_queues[get_current_city_name()])
    short_pause()
    close_all_windows()


def do_auto_recruit():
    connect()
    print_with_time_and_color('\n--do_auto_recruit--', 'blue')
    for e in get_current_city_next_recruiting_order():
        unit, amount = e['unit'], e['amount']
        if unit in get_naval_units_list():
            open_docks()
            print("Choix de " + unit + " dans le port")
        else: 
            open_barracks()
            print("Choix de " + unit + " dans la caserne")
        driver.execute_script("document.querySelector('#unit_order_unit_hidden').value = " + "'"+unit+"'")
        short_pause()
        print("Choix du nombre d'unités à former")
        get_element('#unit_order_input').send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE)
        get_element('#unit_order_input').send_keys(amount)
        short_pause()
        print('Lancement de la formation')
        get_element('#unit_order_confirm').click()
        short_pause()
        close_all_windows()


def do_auto_festival():
    connect()
    print_with_time_and_color('\n--do_auto_festival--', 'blue')
    open_culture_overview()
    print("Lancement des éventuels festivals")
    get_element('#start_all_celebrations').click()
    short_pause()
    close_all_windows()


def do_auto_triumph():
    connect()
    print_with_time_and_color('\n--do_auto_triumph--', 'blue')
    BP = get_element(
        '.nui_battlepoints_container>.points').get_attribute('innerText')
    if (int(BP) <= BATTLE_POINTS_TO_SPARE):
        print('Pas assez de PC')
        return
    open_culture_overview()
    get_element('#place_celebration_select>.arrow').click()
    short_pause()
    li = driver.find_elements(By.CSS_SELECTOR, '.item-list>.option')
    for e in li:
        if (e.get_attribute('innerText') == 'Marche triomphale'):
            el = e
    el.click()
    print("Lancement des éventuelles marches triomphales")
    get_element('#start_all_celebrations').click()
    short_pause()
    close_all_windows()


def do_auto_farm_towns():
    connect()
    print_with_time_and_color('\n--do_auto_farm_towns--', 'blue')
    open_farm_town_overview()
    print("Récolte des VP de l'île courante")
    get_element('#fto_claim_button').click()
    close_all_windows()


def do_auto_farm_towns_all():
    connect()
    print_with_time_and_color('\n--do_auto_farm_towns_all--', 'blue')
    open_farm_town_overview()
    get_element('a.checkbox.select_all').click()
    short_pause()
    print('Récolte des VP')
    get_element('#fto_claim_button').click()
    global last_farm_town
    last_farm_town = datetime.now().timestamp()
    short_pause()
    close_all_windows()


def do_auto_research():
    connect()
    print_with_time_and_color('\n--do_auto_research--', 'blue')
    next_research = get_current_city_next_research()
    open_academy()
    print('Lancement de la recherche')
    if next_research == 'booty':
        next_research = 'booty_bpv'
    query = '.'+next_research+'~.btn_upgrade'
    get_element(query).click()
    short_pause()
    close_front_window()




#####################################
######## is_ready_functions #########
#####################################

def is_ready_auto_attack():
    connect()
    ready = False
    print_with_time_and_color('\n--is_ready_auto_attack--', 'cyan')
    open_attack_planer()
    nb_atk= int(get_element('.attacks').get_attribute('innerText'))
    if nb_atk == 0:
        print('Aucune attaque planifiée')
    else:
        print('Affichage du plan courant')
        get_element('td.ap_name>a').click()
        short_pause()
        print('Tri des attaques par départ croissant')
        get_element('.send_at').click()
        short_pause()
        row = get_element('ul.attacks_list>li>.row3').get_attribute('innerText')
        t = row[-8:]
        texte_jour = row[9:15]
        h = int(t[:2])
        m = int(t[3:5])
        s = int(t[6:8])
        if (texte_jour == "aujour") and ((h*3600+m*60+s)-(int(datetime.now().strftime('%H'))*3600+int(datetime.now().strftime('%M'))*60+int(datetime.now().strftime('%S')))<=TIME_TO_PREPARE_ATTACK) or ((texte_jour=='demain') and ((((24*3600)-(int(datetime.now().strftime('%H'))*3600+int(datetime.now().strftime('%M'))*60+int(datetime.now().strftime('%S'))))+(h*3600+m*60+s))<=TIME_TO_PREPARE_ATTACK)):
            ready = True
            print('Attaque imminente !')
        else:
            print('Aucune attaque imminente')
    close_all_windows()
    return ready


def is_ready_auto_build():
    connect()
    ready = False
    print_with_time_and_color('\n--is_ready_auto_build--', 'cyan')
    if (get_current_city_building_queue_length() >= MAX_BUILDING_ORDERS):
        print("Nombre d'ordres max. atteint")
        return False
    if (building_queues[get_current_city_name()] != []):
        # open_city_overview()
        open_main()
        print('File de ' + get_current_city_name() + ' : ' +
            str(building_queues[get_current_city_name()]))
        first_in_queue = building_queues[get_current_city_name()][0]
        print('Vérication de la possibilité de la construction de ' + first_in_queue)
        el_to_check = get_element(
            building_check_queries[first_in_queue])
        if ('Impossible' not in el_to_check.get_attribute('innerText')):
            print("La construction de " + first_in_queue + " est prête !")
            ready = True
        else:
            print("La construction de " + first_in_queue + " n'est pas prête !")
        close_all_windows()
    else:
        print('Aucun ordre dans la file de construction !')
    return ready


def is_ready_auto_recruit():
    connect()
    print_with_time_and_color('\n--is_ready_auto_recruit--', 'cyan')
    if (get_current_city_pop() <= MIN_POP_TO_RECRUIT):
        print('Population libre insuffisante')
        return False
    next_order, next_order_pop = get_current_city_next_recruiting_order()
    if (next_order_pop >= MIN_POP_TO_RECRUIT):
        return True
    return False


def is_ready_auto_festival():
    connect()
    print_with_time_and_color('\n--is_ready_auto_festival--', 'cyan')
    return True


def is_ready_auto_triumph():
    connect()
    print_with_time_and_color('\n--is_ready_auto_triumph--', 'cyan')
    return True


def is_ready_auto_farm_towns():
    connect()
    ready = False
    print_with_time_and_color('\n--is_ready_auto_farm_towns--', 'cyan')
    storage = get_current_city_storage()
    ressources = get_current_city_resources()
    if ((ressources['wood']==storage) and (ressources['stone']==storage) and (ressources['iron']==storage)):
        print("L'entrepôt est plein !")
        return False
    open_farm_town_overview()
    cl = get_element('#fto_claim_button').get_attribute('className')
    if 'disabled' not in cl:
        ready = True
    close_all_windows()
    print("VP prêts !" if ready else "VP pas prêts")
    return ready


def is_ready_auto_farm_towns_all():
    connect()
    ready = False
    print_with_time_and_color('\n--is_ready_auto_farm_towns_all--', 'cyan')
    if (datetime.now().timestamp() - last_farm_town < 4*60):
        return False
    open_farm_town_overview()
    cl = get_element('#fto_claim_button').get_attribute('className')
    if 'disabled' not in cl:
        ready = True
    close_all_windows()
    print("Prêt !" if ready else "Pas prêt")
    return ready


def is_ready_auto_research():
    connect()
    ready = False
    print_with_time_and_color('\n--is_ready_auto_research--', 'cyan')
    r = get_current_city_next_research()
    open_academy()
    if r!=None:
        print('La recherche ' + r + ' est prête')
        ready=True
    else:
        print("Aucune recherche n'est prête")
    close_front_window()
    return ready




######################################
######## is_stacked_functions ########
######################################

def is_stacked_auto_build():
    connect()
    print_with_time_and_color('\n--is_stacked_auto_build--', 'green')
    if (get_current_city_building_queue_length() >= MAX_BUILDING_ORDERS):
        print('La file de construction est pleine')
        return True
    if (building_queues[get_current_city_name()] == []):
        print('Aucun ordre dans la file de construction')
        return True
    print("Pas stacked")
    return False


def is_stacked_auto_research():
    connect()
    print_with_time_and_color('\n--is_stacked_auto_research--', 'green')
    if (get_current_city_researching_queue_length() >= MAX_RESEARCHING_ORDERS):
        print('La file de recherche est pleine')
        return True
    needed_unlocked_researches = [e for e in get_current_city_unlocked_researches() if e in researches_to_get[get_current_city_name()]]
    if (needed_unlocked_researches == []):
        print("Toutes les recherches disponibles à ce niveau d'académie ont été faites")
        return True
    print("Pas stacked")
    return False


def is_stacked_auto_recruit():
    connect()
    print_with_time_and_color('\n--is_stacked_auto_recruit--', 'green')
    if (get_current_city_recruiting_queue_length() >= MAX_RECRUITING_ORDERS):
        print('La file de formation est pleine')
        return True
    if (get_current_city_pop <= MIN_POP_TO_RECRUIT):
        print("Population libre insuffisante")
        return True
    print("Pas stacked")
    return False




######################################
########## helper_functions ##########
######################################

def sleep_time_randomizer(seconds, fluctuate):
    t = seconds+random()*fluctuate
    # print('sleep time : ' + str(t))
    return t


def short_pause():
    sleep(sleep_time_randomizer(2, 1))


def long_pause():
    sleep(sleep_time_randomizer(10, 2))


def zoom_out():
    driver.execute_script("document.body.style.zoom='67%'")


def setup_window():
    zoom_out()
    driver.maximize_window()
    open_map()
    open_city_overview()


def get_element(query):
    els = []
    for i in range(10):
        if (els == [] or els == None):
            els = driver.find_elements(By.CSS_SELECTOR, query)
            connect()
            sleep(1)
    return els[0]


def print_with_time_and_color(mes, color='white'):
    buf = ''
    while mes[0] == '\n':
        buf += '\n'
        mes = mes[1:]
    print(buf+datetime.now().strftime('[%H:%M:%S]')+' '+colored(mes, color))


##################################################################################################
##################################################################################################

###########################
########## SETUP ##########
###########################

last_farm_town = 0
last_festival = 0


# researches to get in each city
researches_to_get = literal_eval(open('setup_to_edit/researches_to_get.txt', 'r').read())


# building queries
building_buttons_queries = literal_eval(open('data/building_buttons_queries.txt', 'r').read())
building_check_queries = literal_eval(open('data/building_check_queries.txt', 'r').read())


# units
units = literal_eval(open('data/units.txt', 'r').read())


# goal_armies
goal_armies = literal_eval(open('setup_to_edit/goal_armies.txt', 'r').read())


# building queues
building_queues = literal_eval(open('setup_to_edit/building_queues.txt', 'r').read())
build = open("data/building_queues_backup.txt", "w")
build.write(str(building_queues))
build.close()


# enables/disables the options of the bot
auto_farm_towns_enabled = True
auto_attack_enabled = True
auto_festival_enabled = True
auto_reconnect_enabled = True
auto_build_enabled = True
auto_recruit_enabled = True
auto_research_enabled = True


# swap the digits to change the priority order
actions = {
    '1. Ville 1': {
        0: {'name': 'building_upgrade', 'activated': auto_build_enabled, 'do_function': do_auto_build, 'is_ready_function': is_ready_auto_build, 'is_stacked_function': is_stacked_auto_build},
        1: {'name': 'research', 'activated': auto_research_enabled, 'do_function': do_auto_research, 'is_ready_function': is_ready_auto_research, 'is_stacked_function': is_stacked_auto_research},
        2: {'name': 'unit_order', 'activated': auto_recruit_enabled, 'do_function': do_auto_recruit, 'is_ready_function': is_ready_auto_recruit, 'is_stacked_function': is_stacked_auto_recruit},
    },
    '2. Ville 2': {
        0: {'name': 'building_upgrade', 'activated': auto_build_enabled, 'do_function': do_auto_build, 'is_ready_function': is_ready_auto_build, 'is_stacked_function': is_stacked_auto_build},
        1: {'name': 'research', 'activated': auto_research_enabled, 'do_function': do_auto_research, 'is_ready_function': is_ready_auto_research, 'is_stacked_function': is_stacked_auto_research},
        2: {'name': 'unit_order', 'activated': auto_recruit_enabled, 'do_function': do_auto_recruit, 'is_ready_function': is_ready_auto_recruit, 'is_stacked_function': is_stacked_auto_recruit},
    },
    '3. Ville 3': {
        0: {'name': 'building_upgrade', 'activated': auto_build_enabled, 'do_function': do_auto_build, 'is_ready_function': is_ready_auto_build, 'is_stacked_function': is_stacked_auto_build},
        1: {'name': 'research', 'activated': auto_research_enabled, 'do_function': do_auto_research, 'is_ready_function': is_ready_auto_research, 'is_stacked_function': is_stacked_auto_research},
        2: {'name': 'unit_order', 'activated': auto_recruit_enabled, 'do_function': do_auto_recruit, 'is_ready_function': is_ready_auto_recruit, 'is_stacked_function': is_stacked_auto_recruit},
    },
}


# constants
TIME_BETWEEN_ACTIONS = 2
TIME_TO_PREPARE_ATTACK = 180
BATTLE_POINTS_TO_SPARE = 1000
MAX_BUILDING_ORDERS = 3
MAX_RESEARCHING_ORDERS = 2
MAX_RECRUITING_ORDERS = 6
MIN_POP_TO_RECRUIT = 70

USERNAME = '-Loulou54'
PASSWORD = 'L0uL0u54'




############################
########## SCRIPT ##########
############################

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='exe/chromedriver.exe')
driver.get("https://fr.grepolis.com/")
connect()
driver.maximize_window()
# setup_window()

while True:
    try_action_selector()
    sleep(sleep_time_randomizer(TIME_BETWEEN_ACTIONS, 2))
