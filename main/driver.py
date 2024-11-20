from main.login import login_page
from PyQt6.QtWidgets import QApplication
import sqlite3
import os
import pathlib

# TODO: Add more line edits in sign up dialog, such as name, age, location, email

def main():
    connection = sqlite3.connect('database\\accounts.db')
    cursor = connection.cursor()

    cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='accounts'""")

    tableExists = cursor.fetchall()

    if not tableExists:
        cursor.execute("""CREATE TABLE accounts (
            username text,
            password text
        )""")

    # cursor.execute("INSERT INTO accounts VALUES ('admin','123')")

    app = QApplication([])
    login = login_page.LoginPage()

    connection.commit()
    connection.close()

    login.show()
    app.exec()



if __name__ == "__main__":
    main()