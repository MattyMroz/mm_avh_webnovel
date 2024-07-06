import os
from termcolor import cprint

folder_path = os.path.dirname(os.path.abspath(__file__))
file_list = os.listdir(folder_path)

for file_name in file_list:
    if file_name.startswith("nowy") and file_name.endswith(".txt"):
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "r", encoding="utf-8") as source_file:
            content = source_file.read()

        try:
            with open(file_path, "w", encoding="ANSI") as target_file:
                target_file.write(content)
        except UnicodeEncodeError:
            with open(file_path, "w", encoding="ANSI", errors="ignore") as target_file:
                target_file.write(content)

        # Zamieniono kodowanie pliku na ANSI
        cprint("Zamieniono kodowanie na ANSI:",
               'yellow', attrs=['bold'], end=' ')
        print(file_name)
