import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

# Database connection parameters
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Constants
BLOCKS = {
    'А': 7,
    'Б': 5,
    'В': 6,
    'Г': 5,
    'Д': 5,
    'Е': 6,
    'Ж': 5,
    'И': 7
}

START_FLOOR = 3
END_FLOOR = 24
HOUSE_DEFAULTS = {
    'status': 'available',
    'price': 0,
    'buyer_first_name': None,
    'buyer_last_name': None,
    'buyer_phone_number': None,
    'buyer_spend': 0,
    'how_much_is_left': 0
}

FLOUR_DEFAULTS = {
    'available': 0,
    'sold': 0,
    'not_fully_paid': 0,
    'reserved': 0
}

BLOCK_DEFAULTS = {
    'available': 0,
    'sold': 0,
    'not_fully_paid': 0,
    'reserved': 0
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()


def clean_database():
    cur.execute("TRUNCATE TABLE bulding_house, bulding_block, bulding_flour RESTART IDENTITY CASCADE;")
    conn.commit()
    print("Database cleaned.")


def create_data():
    for floor_num in range(START_FLOOR, END_FLOOR + 1):
        cur.execute(
            "INSERT INTO bulding_flour (number, available, sold, not_fully_paid, reserved) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
            (floor_num, FLOUR_DEFAULTS['available'], FLOUR_DEFAULTS['sold'], FLOUR_DEFAULTS['not_fully_paid'], FLOUR_DEFAULTS['reserved'])
        )
        flour_id = cur.fetchone()[0]

        for block_name, home_count in BLOCKS.items():
            cur.execute(
                "INSERT INTO bulding_block (name, flour_id, available, sold, not_fully_paid, reserved) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;",
                (block_name, flour_id, BLOCK_DEFAULTS['available'], BLOCK_DEFAULTS['sold'], BLOCK_DEFAULTS['not_fully_paid'], BLOCK_DEFAULTS['reserved'])
            )
            block_id = cur.fetchone()[0]

            for num_in_block in range(1, home_count + 1):
                house_number = f"{floor_num}{block_name}{num_in_block}"
                cur.execute(
                    sql.SQL(
                        "INSERT INTO bulding_house (number, block_id, flour_id, num_in_block, status, price, buyer_first_name, buyer_last_name, buyer_phone_number, buyer_spend, how_much_is_left) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"),
                    (house_number, block_id, flour_id, num_in_block, HOUSE_DEFAULTS['status'], HOUSE_DEFAULTS['price'],
                     HOUSE_DEFAULTS['buyer_first_name'], HOUSE_DEFAULTS['buyer_last_name'],
                     HOUSE_DEFAULTS['buyer_phone_number'],
                     HOUSE_DEFAULTS['buyer_spend'], HOUSE_DEFAULTS['how_much_is_left'])
                )
                print(f"Created House {house_number} in Block {block_name}, Floor {floor_num}")

    conn.commit()


if __name__ == '__main__':
    clean_database()
    create_data()

# Close the cursor and connection
cur.close()
conn.close()
