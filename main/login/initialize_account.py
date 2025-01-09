import sqlite3
import json

class InitializeAccount:
    def __init__(self, account_id):
        self.account_id = account_id

    def initialize(self):
        self.initialize_to_watch_media_table()
        self.initialize_reviews_table()
        self.initialize_liked_media_table()

    def initialize_liked_media_table(self):
        connection = sqlite3.connect('database\\accounts.db')
        cursor = connection.cursor()

        # Check if row with account_id exists in liked_media table
        does_row_with_account_id_exist = cursor.execute("""SELECT * FROM liked_media WHERE account_id=(:account_id)""",
                                               {"account_id": self.account_id}).fetchone()

        if not does_row_with_account_id_exist:
            liked_movies_json_placeholder = json.dumps([])
            liked_tv_shows_json_placeholder = json.dumps([])

            cursor.execute("""INSERT INTO liked_media VALUES (:account_id, :liked_movies, :liked_tv_shows)""",
                           {"account_id": self.account_id, "liked_movies": liked_movies_json_placeholder,
                            "liked_tv_shows": liked_tv_shows_json_placeholder})

        connection.commit()
        connection.close()

    def initialize_to_watch_media_table(self):
        connection = sqlite3.connect('database\\accounts.db')
        cursor = connection.cursor()

        # Check if row with account_id exists in liked_media table
        does_row_with_account_id_exist = cursor.execute("""SELECT * FROM media_to_watch WHERE account_id=(:account_id)""",
                                                        {"account_id": self.account_id}).fetchone()

        if not does_row_with_account_id_exist:
            movies_to_watch_json_placeholder = json.dumps([])
            tv_shows_to_watch_json_placeholder = json.dumps([])

            cursor.execute("""INSERT INTO media_to_watch VALUES (:account_id, :movies_to_watch, :tv_shows_to_watch)""",
                           {"account_id": self.account_id, "movies_to_watch": movies_to_watch_json_placeholder,
                            "tv_shows_to_watch": tv_shows_to_watch_json_placeholder})

        connection.commit()
        connection.close()

    def initialize_reviews_table(self):
        connection = sqlite3.connect('database\\accounts.db')
        cursor = connection.cursor()

        # Check if row with account_id exists in liked_media table
        does_row_with_account_id_exist = cursor.execute(
            """SELECT * FROM reviews WHERE account_id=(:account_id)""",
            {"account_id": self.account_id}).fetchone()

        if not does_row_with_account_id_exist:
            movie_reviews_json_placeholder = json.dumps({})

            # movie_ids_json_placeholder = json.dumps([])
            # movie_reviews_json_placeholder = json.dumps([])

            tv_show_reviews_json_placeholder = json.dumps({})

            # tv_show_ids_json_placeholder = json.dumps([])
            # tv_show_reviews_json_placeholder = json.dumps([])

            cursor.execute("""INSERT INTO reviews VALUES (:account_id, :movie_reviews, :tv_show_reviews)""",
                           {"account_id": self.account_id, "movie_reviews": movie_reviews_json_placeholder,
                            "tv_show_reviews": tv_show_reviews_json_placeholder})

        connection.commit()
        connection.close()
