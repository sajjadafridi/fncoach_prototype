import PySimpleGUI as sg
import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pandas_profiling


### SCRAPING ###

def update_weapon_list():
    weapons_url = 'https://db.fortnitetracker.com/weapons'
    weapons_page = requests.get(weapons_url)
    soup = BeautifulSoup(weapons_page.content, 'html.parser')
    weapons = []
    for weapon in soup.find_all('h3', class_="trn-card__header-title"):
        weapon_title = weapon.text
        weapons.append(weapon_title)
        weapons.sort()
    return weapons


def update_locations_list():  # TODO find a better way of scraping current locations instead of all
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
    locations.sort()
    return locations


### ANALYSIS ###

def analyze_data(user_db):
    user_data_df = pd.read_sql_query(f"SELECT * FROM {user_db}", conn)
    print(user_data_df.profile_report()) # TODO fix memory error


# TODO analzye the data in some kind of meaningful way when the player requests it

### GUI ###

sg.change_look_and_feel('DarkBlue')

data_entry_layout = [
    [sg.Text('FNCoach')],
    [sg.Text('Where did you die?', size=(21, 1)), sg.Combo(update_locations_list(), key='_DEATH_LOCATION_')],
    [sg.Text('What weapon did you die to?', size=(21, 1)), sg.Combo(update_weapon_list(), key='_DEATH_WEAPON_')],
    # TODO add selector for mode (solos, duos, squads), update placement based on this
    [sg.Text('What placement did you get?', size=(21, 1)),
     sg.Combo([i for i in range(1, 101)][::-1], key='_PLACEMENT_')],
    [sg.Text('Try to keep your summary and prevention descriptions under 10 words.', font=('', 8))],
    [sg.Text('Summarize your death.', size=(21, 1)), sg.InputText(key='_DEATH_SUMMARY_')],
    [sg.Text('How can you prevent this?', size=(21, 1)), sg.InputText(key='_PREVENTION_')],
    [sg.Button('Submit'), sg.Button('ResetDB'), sg.Button('Analyze'), sg.Button('Cancel')]
]

layout = [[sg.Frame('Input', data_entry_layout)]]
window = sg.Window('FNCoach', layout)

### SQL ###

conn = sqlite3.connect('fncoach.db')
c = conn.cursor()

c.execute(''' CREATE TABLE IF NOT EXISTS user_data (death_location text, death_weapon text, 
    placement real, death_summary text, prevention text) ''')

app_running = True
while app_running:
    event, user_data = window.read()
    if event == 'Submit':
        user_data_tuple = (user_data['_DEATH_LOCATION_'], user_data['_DEATH_WEAPON_'],
                           int(user_data['_PLACEMENT_']), user_data['_DEATH_SUMMARY_'], user_data['_PREVENTION_'])
        c.execute('INSERT INTO user_data VALUES (?,?,?,?,?);', user_data_tuple)
        conn.commit()
    elif event == 'ResetDB':
        c.execute('DELETE FROM user_data')
        conn.commit()
    elif event == 'Analyze':
        analyze_data('user_data')
    elif event == 'Cancel':
        app_running = False
    elif event == 'Exit':
        app_running = False

conn.close()
window.close()
