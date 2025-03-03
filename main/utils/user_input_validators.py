import re
import sqlite3


class UserInputValidators:

    @staticmethod
    def login_input_validator(input_username, input_password, all_usernames, all_passwords):

        # TODO: Trim the leading and trailing spaces before checking each field
        if input_username in all_usernames:
            password_index = all_usernames.index(input_username)

            if input_password != all_passwords[password_index]:
                return "Password is wrong."

            elif input_password == "":
                return "Password is blank."

        elif input_username == "":
            return "Username is blank."
        else:
            return "Account doesn't exist."

        return ""

    def signup_input_validator(self, firstname, lastname, email, username, password, confirm_password):
        connection = sqlite3.connect('../database\\accounts.db')
        cursor = connection.cursor()

        all_usernames_tuple = cursor.execute("SELECT username FROM accounts").fetchall()

        # Convert each tuple to string
        all_usernames = [str(account[0]) for account in all_usernames_tuple]

        issues_found = []

        if not self.is_valid_name(firstname):
            issues_found.append("First name format is invalid")

        if not self.is_valid_name(lastname):
            issues_found.append("Last name format is invalid")

        if email == "":
            issues_found.append("Email is blank")
        elif not self.is_valid_email(email):
            issues_found.append("Email format is invalid")

        if username == "":
            issues_found.append("Username is blank")
        elif username in all_usernames:
            issues_found.append("Username already exists")

        if password == "":
            issues_found.append("Password is blank")
        elif password == "":
            issues_found.append("Confirm password is blank")
        elif password != confirm_password:
            issues_found.append("Password and confirm password is not equal")

        connection.commit()
        connection.close()

        return issues_found

    @staticmethod
    def is_valid_email(email):
        valid_email = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

        return True if valid_email else False

    @staticmethod
    def is_valid_name(name):
        valid_name = re.match(r'^[a-zA-Z ]+$', name)

        return True if valid_name else False
