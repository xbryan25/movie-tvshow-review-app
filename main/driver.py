from main.login import login_page
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication([])
    login = login_page.LoginPage()


    login.show()
    app.exec()



if __name__ == "__main__":
    main()