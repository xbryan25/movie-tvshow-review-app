from main.login import login_page
from PyQt6.QtWidgets import QApplication
import sqlite3


def main():
    connection = sqlite3.connect('database\\accounts.db')
    cursor = connection.cursor()

    cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='accounts'""")

    tableExists = cursor.fetchall()

    if not tableExists:
        cursor.execute("""CREATE TABLE accounts (
            username text,
            password text,
            firstname text,
            lastname text,
            email text,
            age integer,
            gender text
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