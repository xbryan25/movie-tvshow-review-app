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
            account_id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            firstname TEXT,
            lastname TEXT,
            email TEXT,
            age INTEGER,
            gender TEXT
        )""")

        cursor.execute("""CREATE TABLE liked_media (
                            account_id INTEGER,
                            liked_movies TEXT,
                            liked_tv_shows TEXT,
                            FOREIGN KEY(account_id) REFERENCES accounts(account_id)
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