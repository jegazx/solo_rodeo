import PySimpleGUI as sg
from backend import *

layout = [
    [sg.Text('Zaidimu kolekcijos valdymas')],
    [sg.Button('Prideti zaidima'), sg.Button('Perziureti zaidimus'),
    sg.Button('Ieskoti zaidimo'), sg.Button('Istrinti zaidima'), sg.Button('Atnaujinti zaidima')],
    [sg.Listbox(values=[], size=(50, 10), key='-LIST-', enable_events=True)],
    [sg.Exit()]
]

window = sg.Window('Zaidimu kolekcijos valdymas', layout)

def open_add_game_window():
    layout = [
        [sg.Text('Zaidimo pavadinimas:'), sg.Input(key=("-NAME-"))],
        [sg.Text('Kurejas:'), sg.Combo(esami_kurejai(), key='-KUREJAS-')],
        [sg.Text('Zanras:'), sg.Listbox(esami_zanrai(), key='-ZANRAS-', select_mode='multiple')],
        [sg.Text('Arba iveskite nauja zanra:'), sg.Input(key='-NAUJAS_ZANRAS-')],
        [sg.Text('Youtube video nuoroda'), sg.Input(key='-YOUTUBE-')],
        [sg.Button('Prideti'), sg.Button('Atsaukti')]
    ]
    return sg.Window('Prideti zaidima', layout)

while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break

    elif event == 'Prideti zaidima':
        add_game_window = open_add_game_window()
        while True:  # pridedame dar vieną ciklą skaityti iš antrinio lango
            add_event, add_values = add_game_window.read()
            if add_event in (sg.WINDOW_CLOSED, 'Atsaukti'):
                add_game_window.close()
                break
            elif add_event == 'Prideti':
                if add_values['-NAME-'].strip() == "":
                    sg.popup("Klaida: Iveskite zaidimo pavadinima")
                zaidimo_pavadinimas = add_values['-NAME-']
                kurejas = add_values['-KUREJAS-']
                zanras = add_values['-NAUJAS_ZANRAS-']
                youtube_link = add_values['-YOUTUBE-']
                add_game(zaidimo_pavadinimas, kurejas, zanras, youtube_link)
                add_game_window.close()
                break

    elif event == 'Perziureti zaidimus':
        pass
    
    elif event == 'Ieskoti zaidimo':
        pass

    elif event == 'Istrinti zaidima':
        pass
    
    elif event == 'Atnaujinti zaidima':
        pass

if window is not None:
    window.close()
