links = "https://bednovel.com/bednovel/shadow-slave-76380/ch"
def num_url():
    with open('webs3.txt', 'w', encoding='utf-8') as f:
        for i in range(1001, 1050+1):
            f.write(links + str(i) + "\n")
    f.close()
num_url()

