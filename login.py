# -*- encoding: utf-8 -*-
import requests
import configparser
from tkinter import messagebox, Tk, Frame, Label, Entry, TOP, LEFT, RIGHT, X, YES, Button
from bs4 import BeautifulSoup


logoutPayload = {}
fields = ['Username','','User'], ['Password','*',''], ['URL','','http://10.100.0.1:8002/index.php?zone=lan_negar']

def login(user, password, url):

    #headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'auth_user':user,'auth_pass':password,'redirurl':'http://blog.abyz.ir', 'accept':'submit'}

    #session = requests.Session()
    resp = requests.post(url,data=payload)
    print(resp.status_code)
    print(resp.history)

    chunk_size = 1000
    with open("a.html", 'wb') as fd:
        for chunk in resp.iter_content(chunk_size):
            fd.write(chunk)


    soup = BeautifulSoup(resp.text, 'html.parser')

    
    if soup.title is None :
        print('Unsucessfull')
        print(soup.find(id='statusbox').find('b').string.strip())
        messagebox.showinfo("Result", "Unsucessfull: " + soup.find(id='statusbox').find('b').string.strip())
    elif "Redirecting" in soup.title.string:
        print('Sucessfull')
        saveConfig(user, password, url)
        messagebox.showinfo("Result", "Sucessfull")
    else:
        print(soup.title.string)



def fetch(entries):
    user = ''
    password = ''
    url = ''
    for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        if   field == 'Username':
            user = text
        elif field == 'Password':
            password = text
        elif field == 'URL':
            url = text

    login(user, password, url)

def makeform(root, fields):
    entries = []
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=15, text=field[0], anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        ent.config(show=field[1])
        ent.insert(0, field[2])
        entries.append((field[0], ent))
    return entries


def getConfig():
    config = configparser.ConfigParser()
    config.read('config.ini')

    if len(config.sections()) > 0:
        fields[0][2] = config['lg']['user']
        fields[1][2] = config['lg']['pass']
        fields[2][2] = config['lg']['url']
    else:
        print('There was an error opening the config file!')
        config['lg'] = {'user': 'tst', 'pass': 'tst','url': 'http://10.100.0.1:8002/index.php?zone=lan_negar'}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)


def saveConfig(user, password, url):
    config = configparser.ConfigParser()
    config['lg'] = {'user': user, 'pass': password,'url': url}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def main():
    getConfig()
    root = Tk()
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))

    b1 = Button(root, text='Login',
          command=(lambda e=ents: fetch(e)))
    b1.pack(side=LEFT, padx=5, pady=5)

    # b2 = Button(root, text='Logout',
    #       command=(lambda e=ents: fetch(e)))
    # b2.pack(side=LEFT, padx=5, pady=5)

    b3 = Button(root, text='Quit', command=root.quit)
    b3.pack(side=LEFT, padx=5, pady=5)
    root.mainloop()

if __name__ == '__main__':
    main()
