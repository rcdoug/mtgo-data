import psycopg
from dotenv import load_dotenv
import os

def execute_query():
    # Load environment variables from .env file
    load_dotenv()

    # Database connection details
    DB_CONN_STR = os.getenv("DB_CONN_STR")


    with psycopg.connect(DB_CONN_STR) as conn:

        with conn.cursor() as cur:
            value = cur.execute("select * from cards").fetchone()
            conn.commit()

    return value


def get_player_ids(player_list: list[str]) -> dict[str, int]:
    """Returns corresponding IDs for a list of player names. Inserts non-present players into table.

    :players: list of player usernames 
    :return: [(player_one_id, player_one_name), (player_two_id, player_two_id), ...]
    """
    load_dotenv()

    # Database connection details
    DB_CONN_STR = os.getenv("DB_CONN_STR")


    with psycopg.connect(DB_CONN_STR) as conn:
        with conn.cursor() as cur:
            sql = "INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING;"
            players_to_insert = [(name,) for name in player_list]
            cur.executemany(sql, players_to_insert)
            
            sql = "SELECT player_id, username FROM players WHERE username =  ANY (%s)"
            cur.execute(sql, [player_list])
            
            results = cur.fetchall()

            player_map = {username: player_id for player_id, username in results}

            return player_map


def insert_event(format_id, event_type_id, date, entries, mtgo_event_id):
    """Used to insert an event.

    :format_id: int, references format table. Can't be NULL
    :event_type_id: int, references event type table. Can't be NULL
    :date: date in ISO format. Can't be NULL
    :entries: int, number of players/decks entered into event. Can't be NULL
    :mtgo_event_id: int, event ID used by MTGO, optional
    :return: int event_id (primary key, distinct from mtgo_event_id)
    """

    return

def get_event_by_mtgo_id(mtgo_event_id: int) -> int:
    """Used to retrieve an event using the mtgo_event_id."""
    event_id = 0
    return event_id

def insert_deck(event_id: int, player_id: int, archetype_id: int, placement: int) -> int:
    """Inserts a deck into decks table.

    :event_id: int, references events table. Can't be NULL
    :player_id: int, references players table. Can't be NULL
    :archetype_id: int, references archetypes table.
    :placement: int, final placement of deck in event. Can't be NULL
    :return: int, decklist_id
    """

    return

if __name__ == "__main__":
    write_entry()