import PySimpleGUI as sg
import pandas as pd
import requests
from bs4 import BeautifulSoup

### SCRAPING ###

def update_weapon_list():
    weapons_url = 'https://db.fortnitetracker.com/weapons'
    weapons_page = requests.get(weapons_url)
    soup = BeautifulSoup(weapons_page.content, 'html.parser')
    weapons = []
    for weapon in soup.find_all('h3', class_="trn-card__header-title"):
        weapon_title = weapon.text
        weapons.append(weapon_title)
    return weapons

def update_locations_list():
    locations_url = 'https://fortnite.fandom.com/wiki/Locations_(Battle_Royale)'
    locations_page = requests.get(locations_url)
    soup = BeautifulSoup(locations_page.content, 'html.parser')
    locations = []
    for page_content in soup.find_all('div', class_='mw-content-ltr mw-content-text'):
        for location_list_unordered in page_content.find_all('ul'):
            for location_a in location_list_unordered.find_all('a'):
                if location_a != None:
                    locations.append(location_a.text)
    set(locations)
    return locations

### GUI ###

sg.change_look_and_feel('DarkBlue')

data_entry_layout = [
    [sg.Text('FNCoach')],
    [sg.Text('Where did you die?', size=(21,1)), sg.Combo(update_locations_list(), key='_DEATH_LOCATION_')],
    [sg.Text('What weapon did you die to?', size=(21,1)), sg.Combo(update_weapon_list(), key='_DEATH_WEAPON_')],
    [sg.Text('What placement did you get?', size=(21,1)), sg.Combo([i for i in range(1,101)][::-1],key='_PLACEMENT_')],
    [sg.Text('Summarize your death.', size=(21,1)), sg.Multiline(key='_DEATH_SUMMARY_')],
    [sg.Text('How can you prevent this?', size=(21,1)), sg.Multiline(key='_PREVENTION_')],
    [sg.Button('Submit'), sg.Button('ResetDF'), sg.Button('Cancel')]
]

layout = [[sg.Frame('Input', data_entry_layout)]]
window = sg.Window('FNCoach', layout)

### PANDAS ###

# CREATE DATAFRAME
user_data_dict = {'death_location':[],'death_weapon':[],
             'placement':[], 'death_summary':[], 'prevention':[]}

app_running = True
while app_running:
    event, user_data = window.read()
    if event == 'Submit':
        user_data_dict['death_location'].append(user_data['_DEATH_LOCATION_'])
        user_data_dict['death_weapon'].append(user_data['_DEATH_WEAPON_'])
        user_data_dict['placement'].append(user_data['_PLACEMENT_'])
        user_data_dict['death_summary'].append(user_data['_DEATH_SUMMARY_'])
        user_data_dict['prevention'].append(user_data['_PREVENTION_'])
        df = pd.DataFrame(user_data_dict)
        print(user_data_dict)

    elif event == 'ResetDF':
        df.iloc
    elif event == 'Cancel':
        app_running = False
    elif event == 'Exit':
        app_running = False

window.close()