#!/usr/bin/env python

__authors__ = "Nicolas"
__contact__ = "nico1801.mf2@gmail.com"
__version__ = "1.0.0"
__date__ = "2022"

import math
import os
from configparser import ConfigParser
import sys
import getopt
import sqlite3
import hashlib
from os.path import getsize
from os import walk
from tkinter import Tk, Label, messagebox, Button, PhotoImage, Canvas
from tkinter.constants import BOTTOM, NW

from PIL import Image, ImageTk

"""
Search duplicate picture.

Code test on pyvala
$ pylava duplicate.py
$

Code test with doctest
$ python -m doctest duplicate.py
$

Code performance test with cProfile
python -m cProfile duplicate.py

Usage:
======
    python duplicate.py -r pathDirectory    
"""

###########################################
#  Definition des constantes              #
###########################################
OPEN_SUCCESS = "Opened database successfully"
OPERATION_SUCCESS = "Operation done successfully"
REQUEST = "SELECT id, name, address, salary from COMPANY"
FILE_2_SIGN = "Lenna.png"
QUIT_WINDOW = False
index = 0


###########################################
#  Gestion de l'affichage txt             #
###########################################
def print_hi(show_val_hs, show_name):
    """
    :param show_val_hs: 
    :param show_name: 
    :return: 
    
     >>> print_hi(1, "Nico")
    Hi, Nico your score is 1
    """

    print(f'Hi, {show_name} your score is {show_val_hs}')


def check_args(argv):
    try:
        return getopt.getopt(argv, "hs:n:", ["HighScore=", "name="])
    except getopt.GetoptError:
        print('duplicate.py -hs <HighScore> -n <Name>')
        sys.exit(2)


def create_db(db_name):
    conn = sqlite3.connect(db_name)
    try:
        conn.execute('''DROP TABLE DUPLICATE_FILE;''')
        conn.execute('''CREATE TABLE DUPLICATE_FILE 
        (ID_SHA CHAR(64) NOT NULL,
        NAME    TEXT     NOT NULL,
        PATH    TEXT     NOT NULL,
        SIZE    INT      NOT NULL);''')
        conn.execute('''create index index_id_sha on specified 
        DUPLICATE_FILE (ID_SHA);''')
    except sqlite3.OperationalError:
        print("Table already exist")
    conn.close()


def add_file_db(db_name, file_id_sha, file_name, file_path, file_size):
    conn = sqlite3.connect(db_name)
    request = "INSERT INTO DUPLICATE_FILE (ID_SHA, NAME, PATH, SIZE) " \
              "VALUES ('" + file_id_sha + "', '" + file_name + \
              "', '" + file_path + "', " + str(file_size) + ")"
    conn.execute(request)
    conn.commit()
    conn.close()


def provide_list_sha_duplicate_file(db_name):
    conn = sqlite3.connect(db_name)
    request = "select count(ID_SHA), ID_SHA from DUPLICATE_FILE " \
              "group by ID_SHA"
    cursor = conn.execute(request)
    list_sha_duplicate_file = []
    for row in cursor:
        if row[0] > 1:
            list_sha_duplicate_file.append(row[1])
    conn.close()
    return list_sha_duplicate_file


def provide_list_duplicate_file(db_name, file_id_sha):
    conn = sqlite3.connect(db_name)
    request = "select ID_SHA, NAME, PATH, SIZE from DUPLICATE_FILE " \
              "where ID_SHA = '" + file_id_sha + "'"
    cursor = conn.execute(request)
    list_duplicate_file = []
    for row in cursor:
        file_description = (row[0], row[1], row[2], row[3])
        list_duplicate_file.append(file_description)
    conn.close()
    return list_duplicate_file


def search_file_id_sha(file_name):
    with open(file_name, "rb") as f:
        file_bytes = f.read()
        result = hashlib.sha256(file_bytes)
        return result.hexdigest()


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def label_image(master, image_path):
    if not os.path.exists(path):
        raise IOError("file {} does not exist".format(image_path))
    print(f"{image_path}")
    photo = PhotoImage(file=image_path)
    canvas = Canvas(master, width=photo.width(), height=photo.height())
    my_img = canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.itemconfigure(my_img, image=photo)
    canvas.pack()

    """
    im = Image.open(image_path)
    image = ImageTk.PhotoImage(im)
    pic_label = Label(master)
    pic_label.img = image
    pic_label.config(image=pic_label.img)
    return pic_label
    """


def action_button(master, message, func, param):
    return Button(
        master,
        text=message,
        command=lambda: func(param),
        activeforeground="green",
        activebackground="yellow",
        padx=8,
        pady=5
    )


def action_button_nav(master, message, func, param):
    btn = Button(
        master,
        text=message,
        command=lambda: func(param),
        activeforeground="green",
        activebackground="yellow",
        padx=8,
        pady=5
    )
    btn.pack(side=BOTTOM)


def action_button_next(master, message, func, param):
    btn = Button(
        master,
        text=message,
        command=lambda: func(param),
        activeforeground="green",
        activebackground="yellow",
        padx=8,
        pady=5
    )
    btn.pack(side=BOTTOM)


def action_button_prev(master, message, func, param):
    btn = Button(
        master,
        text=message,
        command=lambda: func(param),
        activeforeground="green",
        activebackground="yellow",
        padx=8,
        pady=5
    )
    btn.pack(side=BOTTOM)


def msg_call_back(message):
    messagebox.showinfo("App", "Le bouton à " + message + " est cliqué")


def close_main_window(master):
    global QUIT_WINDOW
    QUIT_WINDOW = True
    master.quit()


def show_picture_next(list_duplicate_file):
    global index
    index = index + 1
    val_index_max = len(list_duplicate_file) - 1
    if index > val_index_max:
        index = val_index_max
    show_picture(list_duplicate_file)


def show_picture_prev(list_duplicate_file):
    global index
    index = index - 1
    if index < 0:
        index = 0
    show_picture(list_duplicate_file)


def show_picture(list_duplicate_file):
    (id_sha, file_name, file_path, size) = list_duplicate_file[index]
    print(f" id:{id_sha} name:{file_name} path:{file_path} "
          f"size:{convert_size(size)} index:{index}")
    picture = os.path.join(file_path, file_name)
    label = Label(root, text=picture, bg="yellow")
    label.pack()
    label_image(root, picture)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    db_base_name = "test.db"
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    if len(sys.argv) > 1:
        val_hs = 0
        name = "PyCharm"
        opts, args = check_args(sys.argv[1:])
        for opt, arg in opts:
            if opt in ("-hs", "--HighScore"):
                val_hs = arg
            elif opt in ("-n", "--name"):
                name = arg
        print_hi(val_hs, name)
    else:
        print_hi(10, 'PyCharm')
    config = ConfigParser()  # On crée un nouvel objet "config".
    config.read('parametres.cfg')  # On lit le fichier de paramètres.
    high_score = config.getint('records', 'high_score')
    print(f"HS : {high_score}")
    file = open('parametres.cfg', 'r+')
    config.set('records', 'high_score',
               str(50))  # enregistrement des variables en mémoire
    config.write(file)
    file.close()
    create_db(db_base_name)
    path = os.getcwd()
    nb_file = 0
    file_process = 0
    for (directory, sub_directory, files) in walk(path):
        nb_file = len(files)
        break
    for (directory, sub_directory, files) in walk(path):
        print(f"File treat {file_process} / {nb_file}")
        for file in files:
            file_process += 1
            file_id = search_file_id_sha(file)
            add_file_db(db_base_name, file_id, file, directory, getsize(file))
        break
    print(f"File treat {file_process} / {nb_file}")
    liste_sha_id = provide_list_sha_duplicate_file(db_base_name)
    liste_duplicate_file = []
    for sha_id in liste_sha_id:
        liste_duplicate_file = \
            provide_list_duplicate_file(db_base_name, sha_id)
    index_max = len(liste_duplicate_file)
    print(f"index max:{index_max}")
    root = Tk()
    root.title("Duplicate picture")
    show_picture(liste_duplicate_file)
    action_button_nav(root, "suivant", show_picture_next, liste_duplicate_file)
    action_button_nav(root, "precedent", show_picture_prev,
                      liste_duplicate_file)
    action_button(root, "info", msg_call_back, "info").pack(side=BOTTOM)
    action_button(root, "quitter", close_main_window, root).pack(side=BOTTOM)
    root.mainloop()
