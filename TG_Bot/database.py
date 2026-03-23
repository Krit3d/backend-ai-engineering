import sqlite3


# Main class containing all methods with SQL-queries
class Database:
    def __init__(self, db_file: str) -> None:
        # Store filename in object
        self.db_file = db_file

        # Instant init of tables when creating an obj
        self._create_tables()

    # Only two tables: users and requests_log
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

    # Enter user data on /start command
    def insert_user(self, user_id: int, full_name: str):
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()

            try:
                cur.execute(
                    "INSERT OR IGNORE INTO users (user_id, full_name) VALUES (?, ?)",
                    (user_id, full_name),
                )
            except sqlite3.Error as e:
                print(f"DB Error: {type(e).__name__}.")

    # Simple check to see if the user is blocked
    def is_user_banned(self, user_id: int) -> bool:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                "SELECT is_banned FROM users WHERE user_id = ?", (user_id,)
            )

            user_data = cur.fetchone()

            # Prevent errors by returning bool answer
            return user_data and user_data[0]

    # Two methods to change user status
    def ban_user(self, user_id: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE users SET is_banned = 1 WHERE user_id = ?", (user_id,)
            )

    def unban_user(self, user_id: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE users SET is_banned = 0 WHERE user_id = ?", (user_id,)
            )

    # Getting list of users by /admin command
    def get_all_users(self) -> list[tuple[int, str]]:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute("SELECT user_id, full_name FROM users")

            users = cur.fetchall()

        return users

    # Just a logging of user's requests
    def write_into_log(self, user_id: int, coin: str) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()

            try:
                cur.execute(
                    "INSERT INTO requests_log (user_id, coin) VALUES (?, ?)",
                    (user_id, coin),
                )
            except sqlite3.Error as e:
                print(f"DB Error: {type(e).__name__}.")

    # Return list of grouped by user name crypto requests(/stats command)
    def get_statistics(self) -> list[str, str, int]:
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
                # Prevent error by explicit setting an empty list
                query_list = []
            else:
                query_list = cur.fetchall()

        return query_list
