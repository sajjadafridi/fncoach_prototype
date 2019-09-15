import PySimpleGUI as sg
import sqlite3

### GUI ###

data_entry_layout = [
    [sg.Text('FNCoach')],
    [sg.Text('Where did you die?', size=(21,1)), sg.InputText(key='_DEATH_LOCATION_')],
    [sg.Text('What weapon did you die to?', size=(21,1)), sg.InputText(key='_DEATH_WEAPON_')],
    [sg.Text('What placement did you get?', size=(21,1)), sg.InputText(key='_PLACEMENT_')],
    [sg.Text('Summarize your death.', size=(21,1)), sg.InputText(key='_DEATH_SUMMARY_')],
    [sg.Text('How can you prevent this?', size=(21,1)), sg.InputText(key='_PREVENTION_')],
    [sg.Button('Submit'), sg.Button('ResetDB'), sg.Button('Cancel')]
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
    event, values = window.read()
    if event == 'Submit':
        user_data = values
        user_data_tuple = (user_data['_DEATH_LOCATION_'], user_data['_DEATH_WEAPON_'],
                           int(user_data['_PLACEMENT_']), user_data['_DEATH_SUMMARY_'], user_data['_PREVENTION_'])
        c.execute('INSERT INTO user_data VALUES (?,?,?,?,?);', user_data_tuple)
        conn.commit()
    elif event == 'ResetDB':
        c.execute('DELETE FROM user_data')
        conn.commit()
    elif event == 'Cancel':
        app_running = False

conn.close()
window.close()