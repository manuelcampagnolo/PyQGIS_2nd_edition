# Simple examples of QtWidgets and QMessageBox for interacting with user
# The QMessageBox class provides a modal dialog for informing the user or for asking the user a question and receiving an answer
# 

from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QInputDialog, QApplication, QLabel)

parent=iface.mainWindow()

# Input text
# If you click the OK button, the Boolean value is true.
text, ok = QInputDialog.getText(parent,'input dialog', 'Type a word')
print(text)

# Input item from drop down list
myoptions=["Cow","Sheep","Goat"] #alternatively, vlayer.dataProvider().fields().names()
myoption, ok = QInputDialog.getItem(parent, "select:", "milk types", myoptions, 0, False)
print(myoption)

# Provide information to user
myvar="Hello"
QMessageBox.information(parent,'Info','My variable is {}'.format(myvar))

# Ask Yes/No question
res=QMessageBox.question(parent,'Question', 'Do you want to continue?' )

if res==QMessageBox.Yes:
    QMessageBox.information(parent,'Your decision',"Let's go")

if res==QMessageBox.No:
    QMessageBox.information(parent,'Your decision',"Let's stop")

