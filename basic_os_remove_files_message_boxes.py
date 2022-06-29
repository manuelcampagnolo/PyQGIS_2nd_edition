# os.remove and message boxes
# delete all files in a given folder: BE CAREFUL!
import os
parent=iface.mainWindow() # necessary for QMessageBox

myfoldertemp=r"C:\Users\mlc\Documents\PyQGIS\temp"

# list all files in folder
QMessageBox.information(parent,'Info', 'Files:'+' '.join(os.listdir(myfoldertemp)))

# ask user to confirm
answer=QMessageBox.question(parent,'Question', 'Do you really want to delete files?' )

if answer==QMessageBox.Yes: 
    # delete all files in folder
    for f in os.listdir(myfoldertemp):
        os.remove(os.path.join(myfoldertemp,f))