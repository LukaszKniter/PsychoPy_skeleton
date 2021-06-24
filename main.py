from psychopy import visual, core, event, gui
import random
import csv
import os, sys
from random import shuffle
from pathlib import Path
import codecs

# zmienne globalne
N_TRIALS_TRAIN = 1
N_TRIALS_EXP = 1
hello_info = 'C:/Users/Laptop/Desktop/Informatyka projekt/welcome.txt'
breake_info = "Przerwa, aby przejść do następnego bloku naciśnij spacje."
aft_train_info = "Koniec treningu, nacinij spację, żeby przejsć do zadania."
end_info = "Koniec, dziękujemy za udział w badaniu!"
# lista z wynikami
RESULTS = list()
RESULTS.append(["IDENTYFIKATOR", "Plec", "Wiek", "EXPERIMENT"])


"""okno startowe w ktorym trzeba podac kilka danych, ID, plec, wiek, ono musi być na poczatku, bo 
inaczej full screen win nam wszystko przysloni, podobno znany problem na forum"""

def poop_up():
    info = {'IDENTYFIKATOR': '', u'P\u0141EC': ['M', "K"], 'WIEK': ''}
    hello_dlg = gui.DlgFromDict(dictionary=info, title='Grupa Zero')
    if not hello_dlg.OK:
        abort_with_error('Info dialog terminated.')
    list = [info['IDENTYFIKATOR'], info['PŁEC'], info['WIEK']]
    RESULTS.append(list)


poop_up()

# okno glowne
win = visual.Window(units="pix", color="white", fullscr=True)
# punkt fiksacji
fix = visual.TextStim(win, text="+", color="black", height=40)

# sciezki do plikow w dwoch folderach happy i angry na dysku
happypath = "C:/Users/Laptop/Desktop/Informatyka projekt/happy"
happy_pictures = list(os.listdir(happypath))
angrypath = "C:/Users/Laptop/Desktop/Informatyka projekt/angry"
angry_pictures = list(os.listdir(angrypath))


# tworzy plik wynikowy
def save_result():
    with open("result.csv", "w", newline='', encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerows(RESULTS)


def happy_zgodny(happy_pictures):  # warunek happy zgodny, w srodku happy, po bokach happy
    shuffle(happy_pictures)
    center = happy_pictures[0]
    left = happy_pictures[1]
    right = happy_pictures[1]
    happy1 = [left, center, right]
    return happy1


def angry_zgodny(angry_pictures):  # warunek angry zgodny, w srodku angry, po bokach angry
    shuffle(angry_pictures)
    center = angry_pictures[0]
    left = angry_pictures[1]
    right = angry_pictures[1]
    angry1 = [left, center, right]
    return angry1


def angry_niezgodny(angry_pictures, happy_pictures):  # warunek angry niezgodny, w srodku angry, po bokach happy
    shuffle(angry_pictures)
    shuffle(happy_pictures)
    center = angry_pictures[0]
    left = happy_pictures[1]
    right = happy_pictures[1]
    angry2 = [left, center, right]
    return angry2


def happy_niezgodny(angry_pictures, happy_pictures):  # warunek happy niezgodny, w srodku happy, po bokach angry
    shuffle(angry_pictures)
    shuffle(happy_pictures)
    center = happy_pictures[0]
    left = angry_pictures[1]
    right = angry_pictures[1]
    happy2 = [left, center, right]
    return happy2


def createBlock():  # tworzenie listy z osmioma warunkami, kazdy z 4 podwojnie na koncu liste mieszamy
    block = [happy_zgodny(happy_pictures),
             happy_zgodny(happy_pictures),
             angry_zgodny(angry_pictures),
             angry_zgodny(angry_pictures),
             angry_niezgodny(angry_pictures, happy_pictures),
             angry_niezgodny(angry_pictures, happy_pictures),
             happy_niezgodny(angry_pictures, happy_pictures),
             happy_niezgodny(angry_pictures, happy_pictures)]
    shuffle(block)
    return block

""" funckja, ktora wyswietla jeden blok, pctureset to zmienna zadeklarowana przez nas, trial1_center to jakas
zmienna i wskazanie sciezki do niej z listy pictureset (tej listy nie mamy w ogole w programie, uzywamy jej tylko tutaj,
prawdziwe dane wskazemy pozniej w petli!, na koncu tworzymy 3 zmienne, do ktorej trafiaja nasze pliki i te zmienne sa 
wyswietlane w oknie win"""

def displaySet(picturesSet):
    trial1_center = os.path.abspath(picturesSet[1])
    trial1_left = os.path.abspath(picturesSet[0])
    trial1_right = os.path.abspath(picturesSet[2])

    srodek = visual.ImageStim(win, image=trial1_center, pos=(0.0, 0.0), size=[300, 377], colorSpace='rgb')
    lewy = visual.ImageStim(win, image=trial1_left, pos=(-310.0, 0.0), size=[300, 377], colorSpace='rgb')
    prawy = visual.ImageStim(win, image=trial1_right, pos=(310.0, 0.0), size=[300, 377], colorSpace='rgb')
    fix.draw()
    win.flip()
    core.wait(0.2)
    srodek.draw()
    prawy.draw()
    lewy.draw()
    win.flip()
    core.wait(0.2)


# Julia: to nie jestem do końca pewna, jak działa, ale przydaje się w show_text i pewnie przyda się przy reakcjach prawa/lewa
def reactions(keys):
    event.clearEvents()
    key = event.waitKeys(keyList=keys)
    return key[0]


def show_text(win, info, wait_key=["space"]):
    info.draw()
    win.flip()
    reactions(wait_key)


def hello_text():
    text_file = codecs.open(hello_info, encoding='utf-8').read()
    show_text(win, info=visual.TextStim(win, text=text_file, pos=(0.0, 0.0), color="black"))


def breake():
    show_text(win, info=visual.TextStim(win, text=breake_info, pos=(0.0, 0.0), color="black"))


def after_training():
    show_text(win, info=visual.TextStim(win, text=aft_train_info, pos=(0.0, 0.0), color="black"))


def end():
    img = visual.TextStim(win, text=end_info, pos=(0.0, 0.0), color="black")
    img.draw()
    win.flip()
    core.wait(1)


"""model eksperymentu - dla 'exp=False' robi trening, jeśli trening ma więcej, niż 1 blok, to pomiędzy blokami 
robi przerwę, a po ostatnim mówi, że pora na eksperyment dla 'exp = True' robi eksperyment z przerwami i informacją 
o zakończeniu po ostatnim bloku"""


def part_of_exp(n_trials, exp):
    for i in range(n_trials):
        for picturesSet in createBlock():
            displaySet(picturesSet)
        if exp == True:
            if i < (N_TRIALS_EXP - 1):
                breake()
            else:
                end()
        else:
            if i < (N_TRIALS_TRAIN - 1):
                breake()
            else:
                after_training()
        RESULTS.append([i + 1, exp])  # dodaje wyniki do pliku wynikowego


hello_text()
part_of_exp(N_TRIALS_TRAIN, exp=False)
part_of_exp(N_TRIALS_EXP, exp=True)
save_result()

win.flip()
win.close()
