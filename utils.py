import sqlite3
import os

#################################################################################
# Définition
conn = sqlite3.connect('db.db')
cur = conn.cursor()
#################################################################################

def close_module():
    os.system("pause")
    os.system("cls")

def clear_console():
    os.system("cls")