# Kopiowanie i przetłumacznie tekstu z linków do stron internetowych

# pip install -U selenium
# pip install googletrans
# pip install googletrans==3.1.0a0
# pip install requests
# pip install bs4
# pip install --upgrade deepl
# pip install pyperclip
# pip install pyautogui
# pip install termcolor
# ChromeDriver z twoją wersją Chrome -> C:\ Program Files (x86)\chromedriver.exe

# IMPORTOWANIE MODUŁÓW
from bs4 import BeautifulSoup
import requests
import contextlib
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from googletrans import Translator
import time
import deepl
import pyperclip
import pyautogui
import subprocess
import nltk
from termcolor import cprint

# ----------------------------------------------
#                ZMIENNE GLOBALNE
# ----------------------------------------------
#            USTAWIENIA PRZEGLĄDARKI
# ----------------------------------------------

# PATH = "C:\Program Files (x86)\chromedriver.exe"
# driver = webdriver.Chrome(PATH)

# ----------------------------------------------
#     WYBÓR LINKÓW STRON DO PRZETŁUMACZENIA
# ----------------------------------------------
# 1 = Automatyczne numeracja - webs1
# 2 = Lista stron - webs2

set_websides = 1
# set_websides = 2

# ----------------------------------------------
#       WYBÓR SPOSOBU POBIERANIA TEKSTU
# ----------------------------------------------
# ChromeDriver z twoją wersją Chrome -> C:\ Program Files (x86)\chromedriver.exe
# 1 = Pobieranie poprzez chromedriver - wolniejsze, ale wszędzie działa
# 2 = Pobieranie poprzez requests i bs4 - szybsze, ale nie wszędzie działa jak jest ochrona przed botami

# set_download = 1
set_download = 2

# ----------------------------------------------
#      lICZBA ROZDZIAŁÓW DO PRZETŁUMACZENIA
# ----------------------------------------------
# if set_websides == 1:

first_chapter = 1
last_chapter = 50

# ----------------------------------------------
#    NAZWY KLAS Z KTÓRYCH POBIERZEMY TEKST
# ----------------------------------------------
# zmadaj strone i kliknij prawym na tekst i wybierz "Zbadaj" i wybierz klasę w której jest tekst

# classes = ["book_title", "chapter-title", "chapter-content"]

# dla https://freewebnovel.com/ i https://bednovel.com/
classes = ["tit", "chapter", "txt"]

# dla https://novelbin.net
# classes = ["novel-title", "chr-text", "chr-c"]

# ----------------------------------------------
#   PODZIAŁ - ILE ROZDZIAŁÓW W JEDNYM PLIKU
# ----------------------------------------------

chapters_in_file = 25


# ----------------------------------------------
#           NAZWA PLIKU WYJŚCIOWEGO
# ----------------------------------------------

file_name = "nowy"

# ----------------------------------------------
# NUMER PLIKU WYJŚCIOWEGO I NUMERACJA ROZDZIAŁÓW
# ----------------------------------------------

file_number = 1

# ----------------------------------------------
#         TŁUMACZENIE GOOGLE lub DEEPL
# ----------------------------------------------
# 1 = Google - szybko, ale nie niedokładnie
# 2 = DeepL API Kay - szybko i dokładnie - wymaga klucza API DeepL
# 3 = DeepL Free Desktop - wolno i dokładnie - wymaga instalacji DeepL Desktop

set_translate = 1
# set_translate = 2
# set_translate = 3

# ----------------------------------------------
#   ILE LINII MA BYĆ PRZEŁAMANE JEDNOCZEŚNIE
# ----------------------------------------------
# REKOMENDACJA:
# Google = 50
# DeepL = 15 lub 20 zalerzy od długości jednej linii

# lines_number = 50
# lines_number = 40
lines_number = 25

# ----------------------------------------------
#                 TYTUŁ KSIĄŻKI
# ----------------------------------------------

book_name = "The Beginning After The End"
book_name_pl = "Początek Po Końcu"

# ----------------------------------------------

# GŁÓWNA FUNKCJA


def main():
    start_time = time.time()

    cprint("╚═══ Multimedia Magic – Audio Visual Heaven ═══╝",
           'white', attrs=['bold'])
    print("")
    print("-----------------------------")
    print("Pobiernie danych z linków...")
    select_webs(set_websides)

    # Kopia zapasowa
    with open('0.txt', 'r', encoding="utf-8") as f:
        with open('0_copy.txt', 'w', encoding="utf-8") as f1:
            for line in f:
                f1.write(line)

    if set_translate == 1:
        print("-----------------------------")
        print("Tłumaczenie...")
        translate_google()

    if set_translate == 2:
        print("-----------------------------")
        print("Tłumaczenie...")
        translate_deepl()

    if set_translate == 3:
        print("-----------------------------")
        print("Tłumaczenie...")
        translate_deepl_desktop()

    print("-----------------------------")
    print("Usuwanie wybranych słów i znaków...")
    erasing_words()

    print("-----------------------------")
    print("Podział na pliki - ile rozdziałów w jednym pliku...")
    create_files()
    # create_files_ang()

    print("-----------------------------")
    print("Poprawianie, nadawanie tytułów i numeracji...")
    book_title()

    print("Zakończono :)")
    # Mierz czas
    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s minutes ---" % ((time.time() - start_time) / 60))
    print("--- %s hours ---" % ((time.time() - start_time) / 3600))

# WYBÓR LINKÓW STRON DO PRZETŁUMACZENIA


def select_webs(num):
    if num == 1:
        print("Wybrano 1 = Automatyczne numeracja - webs1.txt")
        webs1 = getWebs(num)
        getData1(webs1)
    elif num == 2:
        print("Wybrano 2 = Lista stron - webs2.txt")
        webs2 = getWebs(num)
        getData2(webs2)
    else:
        print("Nie ma takiej opcji")
        return 0


# POBRANIE LINKÓW STRON


def getWebs(num):
    with open('webs' + str(num) + '.txt', 'r', encoding='utf-8') as f:
        web = f.readlines()

    return web

# POBRANIE DANYCH ZE STRON 1


def getData1(webs1):
    with open('0.txt', 'w', encoding='utf-8') as f:
        f.write("")

    if set_download == 1:
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)

        for i in range(first_chapter, last_chapter + 1):
            print(webs1[0].strip() + str(i) + webs1[1].strip())
            driver.get(webs1[0].strip() + str(i) + webs1[1].strip())
            for i in classes:
                element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CLASS_NAME, i))
                )
                with open('0.txt', 'a', encoding='utf-8') as f:
                    f.write(element.text)
                    f.write("\n")

            driver.quit()
            driver = webdriver.Chrome(PATH)

        driver.quit()

    # Pętla pobierająca dane - nie działa dla https://freewebnovel.com/
    if set_download == 2:
        for i in range(first_chapter, last_chapter + 1):
            print(webs1[0].strip() + str(i) + webs1[1].strip())
            while True:
                try:
                    soup = BeautifulSoup(requests.get(
                        webs1[0].strip() + str(i) + webs1[1].strip()).text, 'html.parser')
                    for class_ in classes:
                        element = soup.find(class_=class_)
                        with open('0.txt', 'a', encoding='utf-8') as f:
                            f.write(element.text)
                            f.write("\n")
                    break  # Przerwanie pętli while po poprawnym pobraniu danych

                except Exception:
                    continue  # Kontynuowanie pętli while w przypadku błędu

        with open('0.txt', 'r', encoding='utf-8') as f:
            text = f.read()
            sentences = nltk.sent_tokenize(text)
            text = "\n".join(sentences)

        with open('0.txt', 'w', encoding='utf-8') as f:
            f.write(text)


# POBRANIE DANYCH ZE STRON 2


def getData2(webs2):
    with open('0.txt', 'w', encoding='utf-8') as f:
        f.write("")

    if set_download == 1:
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        for i in webs2:
            print(i.strip())
            driver.get(i)
            for i in classes:
                element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CLASS_NAME, i))
                )
                with open('0.txt', 'a', encoding='utf-8') as f:
                    f.write(element.text)
                    f.write("\n")

            driver.quit()
            driver = webdriver.Chrome(PATH)

        driver.quit()

    # Pętla pobierająca dane - nie działa dla https://freewebnovel.com/
    if set_download == 2:
        # for i in webs2:
        #     print(i.strip())
        #     soup = BeautifulSoup(requests.get(i.strip()).text, 'html.parser')
        #     for class_ in classes:
        #         element = soup.find(class_=class_)
        #         with open('0.txt', 'a', encoding='utf-8') as f:
        #             f.write(element.text)

        # with open('0.txt', 'r', encoding='utf-8') as f:
        #     text = f.read()
        #     text = text.replace(".", ".\n")
        # with open('0.txt', 'w', encoding='utf-8') as f:
        #     f.write(text)
        for i in webs2:
            print(i.strip())
            while True:
                try:
                    soup = BeautifulSoup(requests.get(
                        i.strip()).text, 'html.parser')
                    for class_ in classes:
                        element = soup.find(class_=class_)
                        with open('0.txt', 'a', encoding='utf-8') as f:
                            f.write(element.text)
                            f.write("\n")
                    break  # Przerwanie pętli while po poprawnym pobraniu danych

                except Exception:
                    continue  # Kontynuowanie pętli while w przypadku błędu
        with open('0.txt', 'r', encoding='utf-8') as f:
            text = f.read()
            # text = text.replace(".", ".\n")
            if "..." in text:
                text = text.replace("...", "...\n")
            else:
                text = text.replace(".", ".\n")
        with open('0.txt', 'w', encoding='utf-8') as f:
            f.write(text)


# TŁUMACZENIE TEKSTU NA POLSKI


def translate_google():
    with open('0.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open('0.txt', 'w', encoding='utf-8') as f:
        for i in range(0, len(lines), lines_number):
            translator = Translator()
            translation = translator.translate(
                "".join(lines[i:i + lines_number]), dest='PL')
            f.write(translation.text)
            f.write("\n")


def translate_deepl():
    # Zamień na swój klucz https://www.deepl.com/pl/pro-api?cta=header-pro-api/ za darmo 5000000 słów miesięcznie
    auth_key = "1df708bf-af10-3e70-e577-b2d4cb763d74:fx"
    translator = deepl.Translator(auth_key)

    with open('0.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open('0.txt', 'w', encoding='utf-8') as f:
        for i in range(0, len(lines), lines_number):
            translation = translator.translate_text(
                "".join(lines[i:i + lines_number]), target_lang='PL')
            with open('0.txt', 'a', encoding='utf-8') as f:
                f.write(translation.text)
                f.write("\n")

    # Tłumacz cały plik txt / docx
    # translator.translate_document_from_filepath(
    #     '0.txt',
    #     'PL_0.txt',
    #     target_lang='PL',
    #     formality='default'
    # )


def translate_deepl_desktop():
    # subprocess.Popen(
    #     r'C:\Users\mateu\AppData\Roaming\0install.net\desktop-integration\stubs\90d46b1a865bf05507b9fb0d2b3698b63cba3a15fbcafd836ab5523e7a3efb99\DeepL.exe')
    # lub
    command = r'C:\Users\mateu\AppData\Roaming\Programs\Zero Install\0install-win.exe'
    args = ['run', '--no-wait',
            'https://appdownload.deepl.com/windows/0install/deepl.xml']
    subprocess.call([command] + args)

    # Zmień jeśli otwieranie DeepL trwa dłużej
    time.sleep(2)

    with open('0.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open('0.txt', 'w', encoding='utf-8') as file:
        file.write("")

    for i in range(0, len(lines), lines_number):
        text = "".join(lines[i:i+lines_number])
        pyperclip.copy(text)

        screen_width, screen_height = pyautogui.size()
        x = screen_width * 0.25
        y = screen_height * 0.5
        pyautogui.moveTo(x, y)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('del')
        pyautogui.hotkey('ctrl', 'v')

        # Zmień jeśli długo trwa tłumaczenie
        time.sleep(6)
        x = screen_width * 0.75
        pyautogui.moveTo(x, y)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        translated_text = pyperclip.paste()
        with open('0.txt', 'a', encoding='utf-8') as out_file:
            out_file.write(translated_text)

    frezes = ["\nPrzetłumaczono z www.DeepL.com/Translator (wersja darmowa)\n",
              "Przetłumaczono z www.DeepL.com/Translator (wersja darmowa)",
              "\nTranslated with www.DeepL.com/Translator (free version)\n",
              "\nTranslated with www.DeepL.com/Translator (free version)"]

    for freze in frezes:
        with open('0.txt', 'r', encoding='utf-8') as in_file:
            text = in_file.read()
            new_text = text.replace(freze, "")

        with open('0.txt', 'w', encoding='utf-8') as out_file:
            out_file.write(new_text)


# USUWANIE WYBRANYCH SŁOWÓW I ZNAKÓW


def erasing_words():
    words = ["(", ")", "[", "]", "<", ">", "{", "}", "\"", "『", "』",
             "…", "「", "」", "„", "”", "«", "»", "...", "*", "'", "〈", "〉", ""]
    with open('0.txt', 'r', encoding='utf8') as f:
        lines = f.readlines()
    with open('0.txt', 'w', encoding='utf8') as f:
        for line in lines:
            for word in words:
                line = line.replace(word, "")
            f.write(line)


# PODZIAŁ NA PLIKI - ILE ROZDZIAŁÓW W JEDNYM PLIKU


def create_files():
    # Numer pliku wyjściowego
    fNum = file_number
    # zmienna do zmiany frazy
    chapter = first_chapter
    # fraza do wyszykiwania
    phrase = "Rozdział " + str(chapter)

    with open('0.txt', 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            if phrase in line:
                # zwiększenie nazwy pliku
                if chapter == first_chapter:
                    fNum = file_number
                else:
                    fNum += 1
                # zwiększenie frazy
                chapter += chapters_in_file
                phrase = "Rozdział " + str(chapter)
                with open(file_name + " " + str(fNum) + '.txt', 'w', encoding='utf8') as f:
                    f.write(line)
            else:
                with open(file_name + " " + str(fNum) + '.txt', 'a', encoding='utf8') as f:
                    f.write(line)


def create_files_ang():
    # Numer pliku wyjściowego
    fNum = file_number
    # zmienna do zmiany frazy
    chapter = first_chapter
    # fraza do wyszykiwania
    phrase = "Chapter " + str(chapter)

    with open('0.txt', 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            if phrase in line:
                # zwiększenie nazwy pliku
                if chapter == first_chapter:
                    fNum = file_number
                else:
                    fNum += 1
                # zwiększenie frazy
                chapter += chapters_in_file
                phrase = "Chapter " + str(chapter)
                with open(file_name + " " + str(fNum) + '.txt', 'w', encoding='utf8') as f:
                    f.write(line)
            else:
                with open(file_name + " " + str(fNum) + '.txt', 'a', encoding='utf8') as f:
                    f.write(line)

# POPRAWIANIE, NADAWANIE TYTUŁÓW I NUMERACJI


def book_title():
    i = file_number
    while True:
        try:
            with open(file_name + " " + str(i) + '.txt', 'r', encoding='utf8') as f:
                lines = f.readlines()
                index = len(lines) - 1
                myException = lines[index]
                lines.pop()
                with open(file_name + " " + str(i) + '.txt', 'w', encoding='utf8') as f:
                    f.writelines(lines)
        except FileNotFoundError:
            with open(file_name + " " + str(i - 1) + '.txt', 'a', encoding='utf8') as f:
                with contextlib.suppress(NameError):
                    f.writelines(myException)
            break
        i += 1
    i = file_number
    while True:
        try:
            phase = book_name + " " + str(i)
            phase += "\n" + book_name_pl
            with open(file_name + " " + str(i) + '.txt', 'r', encoding='utf8') as f:
                lines = f.readlines()

            with open(file_name + " " + str(i) + '.txt', 'w', encoding='utf8') as f:
                f.write(phase)
                f.write("\n")
                f.writelines(lines)

        except FileNotFoundError:
            break
        i += 1


main()
