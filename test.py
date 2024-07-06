# =================================================================================================
# pobieranie tekstu z strony i zapis do pliku
# pip install requests
# pip install bs4
import re
import time
import os
import requests
from bs4 import BeautifulSoup

# https://novelbin.net/
url = "https://novelbin.net/n/supreme-magus-novel/chapter-2193-hold-the-line-part-1"
classes = ["novel-title", "chr-text", "chr-c"]


def get_text(url, classes):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for class_ in classes:
        element = soup.find(class_=class_)
        with open('0.txt', 'a', encoding='utf-8') as f:
            f.write(element.text)
        f.close()

    with open('0.txt', 'r', encoding='utf-8') as f:
        text = f.read()
        text = text.replace(".", ".\n")
    with open('0.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    f.close()


get_text(url, classes)


# =================================================================================================
# łączenie 2 linii w 1 linię i zapis do pliku
def main():
    with open('1.1.txt', 'r') as f:
        for line in f:
            with open('1.1_out.txt', 'a') as f2:
                line = line.strip() + ' = ' + next(f).strip()
                f2.write(line + '\n')


main()

# =================================================================================================
# zamiana słów za i przed zankiem występującym w tej linii


def main():
    with open('1.1_out.txt', 'r') as f:
        for line in f:
            line = line.rstrip()
            if '=' in line:
                before = line.split('=')[0]
                after = line.split('=')[1]
                with open('1.1_out2.txt', 'a') as f2:
                    f2.write(after + ' = ' + before + '\n')


main()


# =================================================================================================
# usuwanie numeracji stron z pliku tekstowego
a = open('3.txt', 'r', encoding='utf8')
b = open('t3.txt', 'w', encoding='utf8')

for line in a:
    if line[0] in '0123456789':
        continue
    else:
        b.write(line)


# =================================================================================================
# Zamień nazwy plików na autonumerowanie zgodne z datą utworzenia
def filenameToTime():
    path = r'C:\Users\mateu\Downloads\SOLO LEVELING WEBTOON PL\R2'
    files = os.listdir(path)
    # dla karzdego pliku w folderze zamień jego nazwe na date modyfikacji co do sekundy z rozszerzeniem jpg jeśli data jest taka sama to dodaj _ + numer
    i = 0
    for file in files:
        # jeśli file kończy się na jpg to zmień nazwe
        # if file.endswith('.jpg'):
        # pobierz date modyfikacji pliku
        date = time.strftime(
            '%Y-%m-%d_%H-%M-%S', time.localtime(os.path.getmtime(path + '\\' + file)))
        # pobierz rozszerzenie pliku
        extension = file.split('.')[-1]
        # zmień nazwe pliku na date sprawżdź czy plik o tej samej nazwie istnieje jeśli tak to dodaj 1 do sekundy
        if not os.path.exists(path + '\\' + date + '.' + extension):
            os.rename(path + '\\' + file, path +
                      '\\' + date + '.' + extension)
        else:
            os.rename(path + '\\' + file, path + '\\' +
                      date + '_' + str(i) + '.' + extension)
            i += 1


def autoNumericFilename():
    path = r'C:\Users\mateu\Downloads\SOLO LEVELING WEBTOON PL\R2'
    files = os.listdir(path)
    n = 1
    # zamień nazwy wszystkich polików z rozszerzeniem jpg na kolejne liczby n
    for file in files:
        # if file.endswith('.jpg'):
        os.rename(path + '\\' + file, path + '\\' + str(n) + '.jpg')
        n += 1


def main():
    filenameToTime()
    autoNumericFilename()


if __name__ == "__main__":
    main()


# =================================================================================================
# folder in autonumeric foder numeric xd

frist = 1
last = 179


def filenameToTime():
    for j in range(frist, last + 1):
        path = r'C:\Users\mateu\Downloads\SOLO LEVELING WEBTOON PL\R' + str(j)
        files = os.listdir(path)
        i = 0
        for file in files:
            # if file.endswith('.jpg'):
            date = time.strftime(
                '%Y-%m-%d_%H-%M-%S', time.localtime(os.path.getmtime(path + '\\' + file)))
            extension = file.split('.')[-1]
            if not os.path.exists(path + '\\' + date + '.' + extension):
                os.rename(path + '\\' + file, path +
                          '\\' + date + '.' + extension)
            else:
                os.rename(path + '\\' + file, path + '\\' +
                          date + '_' + str(i) + '.' + extension)
                i += 1


def autoNumericFilename():
    for j in range(frist, last + 1):
        path = r'C:\Users\mateu\Downloads\SOLO LEVELING WEBTOON PL\R' + str(j)
        files = os.listdir(path)
        n = 1
        for file in files:
            # if file.endswith('.jpg'):
            os.rename(path + '\\' + file, path + '\\' + str(n) + '.jpg')
            n += 1


def main():
    filenameToTime()
    autoNumericFilename()


if __name__ == "__main__":
    main()


# =================================================================================================
# Usuwanie innych znaków niż litery, cyfry i znaki interpunkcyjne można dodać znaków specjalnych
def clean_text(text):
    return re.sub(r'[^a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9,.;:?!@#$%^&*\s\n', '', text)


input_file = '1.txt'
output_file = 'out_1.txt'

with open(input_file, 'r', encoding='utf-8') as f:
    text = f.read()


cleaned_text = clean_text(text)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(cleaned_text)


# =================================================================================================
# Zamień nazwy plików na autonumerowanie zgodne z datą utworzenia
import os

def rename_files_in_directory(directory_path):
    file_list = [file for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
    file_list.sort(key=lambda x: os.path.getctime(os.path.join(directory_path, x)))
    for index, filename in enumerate(file_list):
        new_filename = f'{index + 1:04d}' + os.path.splitext(filename)[1]
        os.rename(os.path.join(directory_path, filename), os.path.join(directory_path, new_filename))
rename_files_in_directory('path')

# W odwrotnej kolejności
import os

def rename_files_in_directory(directory_path):
    file_list = [file for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
    file_list.sort(key=lambda x: os.path.getctime(os.path.join(directory_path, x)), reverse=True)
    for index, filename in enumerate(file_list):
        new_filename = f'{index + 1:04d}' + os.path.splitext(filename)[1]
        os.rename(os.path.join(directory_path, filename), os.path.join(directory_path, new_filename))


# =================================================================================================
# Zamień nazwy plików na autonumerowanie zgodne z datą utworzenia
import os
from PIL import Image

# ścieżka do folderu z obrazami webp
input_folder = "G:\Dyski współdzielone\Dysk_0\Studniówka Elektryk 2023"

# ścieżka do folderu wyjściowego dla obrazów PNG
output_folder = "G:\Dyski współdzielone\Dysk_0\Studniówka Elektryk 2023"

# iteracja przez wszystkie pliki w folderze wejściowym
for filename in os.listdir(input_folder):
    # pomijanie plików, które nie są obrazami webp
    if not filename.endswith(".webp"):
        continue

    # wczytanie obrazu z pliku
    input_path = os.path.join(input_folder, filename)
    image = Image.open(input_path)

    # tworzenie nazwy pliku wyjściowego
    output_filename = os.path.splitext(filename)[0] + ".png"
    output_path = os.path.join(output_folder, output_filename)

    # zapisywanie obrazu w formacie PNG
    image.save(output_path, "PNG")
