import sqlite3


class Database:
    def __init__(self, db_file):
        # Сохраняем имя файла в внутри объекта
        self.db_file = db_file

        # Сразу при создании объекта инициализируем таблицы
        self._create_tables()

    def _create_tables(self):
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY, 
                    user_id INTEGER UNIQUE,
                    full_name TEXT,
                    is_banned INTEGER DEFAULT 0
                )
            """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS requests_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER REFERENCES users(user_id),
                    coin TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

    def insert_user(self, user_id, full_name):
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()

            try:
                cur.execute(
                    "INSERT OR IGNORE INTO users (user_id, full_name) VALUES (?, ?)",
                    (user_id, full_name),
                )
            except sqlite3.Error as e:
                print(f"DB Error: {type(e).__name__}.")

    def is_user_banned(self, user_id):
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                "SELECT is_banned FROM users WHERE user_id = ?", (user_id,)
            )

            user_data = cur.fetchone()

            return user_data and user_data[0]

    def ban_user(self, user_id):
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE users SET is_banned = 1 WHERE user_id = ?", (user_id,)
            )

    def unban_user(self, user_id):
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE users SET is_banned = 0 WHERE user_id = ?", (user_id,)
            )

    def get_all_users(self):
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute("SELECT user_id, full_name FROM users")

            users = cur.fetchall()

        return users

    def write_into_log(self, user_id, coin):
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()

            try:
                cur.execute(
                    "INSERT INTO requests_log (user_id, coin) VALUES (?, ?)",
                    (user_id, coin),
                )
            except sqlite3.Error as e:
                print(f"DB Error: {type(e).__name__}.")

    def get_statistics(self):
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()

            try:
                cur.execute(
                    """
                    SELECT U.full_name, R.coin, COUNT(R.coin) AS search_volume
                    FROM users AS U
                    INNER JOIN requests_log AS R ON R.user_id = U.user_id
                    GROUP BY U.full_name, R.coin
                    ORDER BY search_volume DESC
                """
                )
            except sqlite3.Error as e:
                print(f"DB Error: {type(e).__name__}.")
                query_list = []
            else:
                query_list = cur.fetchall()

        return query_list
