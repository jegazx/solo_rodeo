import PySimpleGUI as sg
from backendtest import *


menu_def = [['Naujas zanras', ['Prideti zanra']], ['Naujas kurejas', ['Prideti kureja']]]

layout = [
    [sg.Menu(menu_def)],
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
        [sg.Text('Kurejas:'), sg.Combo(esami_kurejai(), size=(15, 5), key='-KUREJAS-')],
        [sg.Text('Zanras:'), sg.Listbox(esami_zanrai(), size=(15, 5), key='-ZANRAS-', select_mode='multiple')],
        [sg.Text('Arba iveskite nauja zanra:'), sg.Input(key='-NAUJAS_ZANRAS-')],
        [sg.Text('Isleidimo metai:'), sg.Input(key='-METAI-')],
        [sg.Text('Youtube video nuoroda'), sg.Input(key='-YOUTUBE-')],
        [sg.Button('Prideti'), sg.Button('Atsaukti')]
    ]
    return sg.Window('Prideti zaidima', layout)

def open_zanras_window():
    layout = [
        [sg.Text('Zanro pavadinimas:'), sg.Input(key='-NAUJAS_ZANRAS-')],
        [sg.Button('Prideti'), sg.Button('Atsaukti')]
    ]
    return sg.Window('Prideti zanras', layout)

def open_kurejas_window():
    layout = [
        [sg.Text('Kurejo pavadinimas:'), sg.Input(key='-KUREJAS-')],
        [sg.Button('Prideti'), sg.Button('Atsaukti')]
    ]
    return sg.Window('Prideti kureja', layout)

headings=['Zaidimo pavadinimas', ' Kurejas', 'Zanras', 'Isleidimo metai']

def all_games_window():
    layout = [
        [sg.Table(values=[], headings=headings, display_row_numbers=False, auto_size_columns=True, num_rows=min(25, len(headings)), key='-ZAIDIMAI-')],
        [sg.Button('Uzdaryti')]
    ]
    window = sg.Window('Visi zaidimai', layout, finalize=True)

    zaidimai = all_games()
    zaidimai_data = [[zaidimas.zaidimo_pavadinimas, zaidimas.kurejas.kurejo_pavadinimas, ",".join(zanras.zanro_pavadinimas for zanras in zaidimas.zanrai), zaidimas.metai]for zaidimas in zaidimai]
    window['-ZAIDIMAI-'].update(zaidimai_data)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Uzdaryti':
            break

    window.close()

while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break

    elif event == 'Prideti zaidima':
        add_game_window = open_add_game_window()
        while True:  
            add_event, add_values = add_game_window.read()
            if add_event in (sg.WINDOW_CLOSED, 'Atsaukti'):
                add_game_window.close()
                break
            elif add_event == 'Prideti':
                if add_values['-NAME-'].strip() == "":
                    sg.popup("Klaida: Iveskite zaidimo pavadinima")
                else:
                    zaidimo_pavadinimas = add_values['-NAME-']
                    kurejas = add_values['-KUREJAS-']
                    zanras = add_values['-ZANRAS-']
                    naujas_zanras = add_values['-NAUJAS_ZANRAS-']
                    metai = add_values['-METAI-']
                    youtube_link = add_values['-YOUTUBE-']
                    if naujas_zanras:
                        zanras.append(naujas_zanras)
                    zanras_obj_list = [session.query(Zanras).filter_by(zanro_pavadinimas=zanras).first() for zanras in zanras]
                    add_game(zaidimo_pavadinimas, kurejas, zanras_obj_list, metai, youtube_link)
                    add_game_window.close()
                    break


    elif event == 'Prideti zanra':
        zanras_window = open_zanras_window()
        while True:
            add_event, add_values = zanras_window.read()
            if add_event in (sg.WINDOW_CLOSED, 'Atsaukti'):
                zanras_window.close()
                break
            elif add_event == 'Prideti':
                zanras = add_values['-NAUJAS_ZANRAS-']
                add_zanras(zanras)
                zanras_window.close()
                break

    elif event == 'Prideti kureja':
        kurejas_window = open_kurejas_window()
        while True:
            add_event, add_values = kurejas_window.read()
            if add_event in (sg.WINDOW_CLOSED, 'Atsaukti'):
                kurejas_window.close()
                break
            elif add_event == 'Prideti':
                kurejas = add_values['-KUREJAS-']
                add_kurejas(kurejas)
                kurejas_window.close()
                break

    elif event == 'Perziureti zaidimus':
        games_window = all_games_window()
    
    elif event == 'Ieskoti zaidimo':
        pass

    elif event == 'Istrinti zaidima':
        pass
    
    elif event == 'Atnaujinti zaidima':
        pass

if window is not None:
    window.close()
