from random import randrange
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn


def create_table(conn, create_table_sql):
    c = conn.cursor()
    c.execute(create_table_sql)


def create_player(conn, player_name):
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE name=(?)", (player_name,))
    rows = cur.fetchall()

    if len(rows) == 0:
        cur.execute("INSERT INTO players (name) VALUES (?)", (player_name,))
        return cur.lastrowid
    else:
        return rows[0][0]


def get_player_average_score(conn, player_id):
    cur = conn.cursor()

    cur.execute("SELECT AVG(score) FROM scores WHERE player_id=(?)", (player_id,))
    rows = cur.fetchall()
    return rows[0][0]


def add_player_score(conn, player_id, score):
    cur = conn.cursor()

    cur.execute("INSERT INTO scores (score, player_id) VALUES (?, ?)", (score, player_id))
    return cur.lastrowid


# Ask the number to the user and ask again if it's not a number
def ask_number():
    result = -1

    while result < 0:
        result = input('Guess it? ')

        # Gére le cas de quelqu'un qui ne saisit pas un nombre
        try:
            result = int(result)
        except ValueError:
            print('This is not a number. Try again.')
            result = -1

    return result


# Check if player has found computer number, display a message and returns if number has been found
def player_has_found(player_number, computer_number, number_of_tries):
    found = False

    if player_number == computer_number:
        found = True
        print('Bravo! You found in', number_of_tries, 'tries!')
    elif player_number > computer_number:
        print('It\'s less.')
    else:
        print('It\'s more.')

    return found


def main():
    # Create a database connection
    database_connection = create_connection("moreorless.db")

    with database_connection:
        # Create players table
        sql_create_players_table = "CREATE TABLE IF NOT EXISTS players (id integer PRIMARY KEY, name text NOT NULL);"
        create_table(database_connection, sql_create_players_table)
        # Create scores table
        sql_create_scores_table = "CREATE TABLE IF NOT EXISTS scores (" \
                                  "id integer PRIMARY KEY, " \
                                  "score integer NOT NULL, " \
                                  "player_id integer NOT NULL, " \
                                  "FOREIGN KEY (player_id) REFERENCES players (id));"
        create_table(database_connection, sql_create_scores_table)

        continue_game = True

        while continue_game:
            # On demande le nom du joueur
            player_name = ''
            while player_name == '':
                player_name = input('What\'s your name? ')

            player_id = create_player(database_connection, player_name)

            print('Hello ', player_name, '! Your average score is ', get_player_average_score(database_connection, player_id), '.', sep='')

            number_found = False
            guess_tries = 0

            number_to_find = randrange(101)

            while not number_found:
                player_choice = ask_number()

                guess_tries += 1

                number_found = player_has_found(player_choice, number_to_find, guess_tries)

            add_player_score(database_connection, player_id, guess_tries)

            restart = input('Restart (Y/n) ? ')
            if restart == 'n' or restart == 'N':
                continue_game = False


if __name__ == '__main__':
    main()
