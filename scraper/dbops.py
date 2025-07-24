import psycopg
from dotenv import load_dotenv
import os

def write_entry():
    # Load environment variables from .env file
    load_dotenv()

    # Database connection details
    DB_CONN_STR = os.getenv("DB_CONN_STR")


    with psycopg.connect(DB_CONN_STR) as conn:

        with conn.cursor() as cur:
            value = cur.execute("select * from cards").fetchone()
            conn.commit()

    return value


def get_player_ids(players):
    """Returns corresponding IDs for a list of player names.

    Inserts non-present players into table.
    :players: list of player usernames 
    :return: [(player_one_id, player_one_name), (player_two_id, player_two_id), ...]
    """

    return


def insert_event(format_id, event_type_id, date, entries, mtgo_event_id):
    """Used to insert an event.

    :format_id: int, references format table
    :event_type_id: int, references event type table
    :date: date in ISO format
    :entries: int, number of players/decks entered into event
    :mtgo_event_id: int, event ID used by MTGO, optional
    :return: int event_id (primary key, distinct from mtgo_event_id)
    """
    
    return

if __name__ == "__main__":
    write_entry()