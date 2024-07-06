with open('0.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    text = text.replace(".", ".\n")
with open('0.txt', 'w', encoding='utf-8') as f:
    f.write(text)