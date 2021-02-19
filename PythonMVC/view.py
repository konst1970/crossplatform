#
# View
#

import model

def view_init():
    print("CRUD, C - Create, R - Read, U - Update, D - Delete, E - exit")

def view_command(message):
    print(message, end = " ")

def view_create():
    print ("Create")

def view_created():
    print ("Element created")
    print (model.read())

def view_read(name):
    print ("Read")
    print (name)

def view_update():
    print ("Update")

def view_delete():
    print ("Delete")
