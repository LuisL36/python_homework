import sqlite3

def create_connection():
    try:
        conn = sqlite3.connect("../db/magazines.db")
        print("Database created and connected successfully")
        return conn
    except sqlite3.Error as e:
        print("Error:", e)
        return None

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        conn.close()

def create_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS publishers (
                publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS magazines (
                magazine_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                publisher_id INTEGER NOT NULL,
                FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                subscriber_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                UNIQUE(name, address)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscriber_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                expiration_date TEXT NOT NULL,
                FOREIGN KEY (subscriber_id) REFERENCES subscribers(subscriber_id),
                FOREIGN KEY (magazine_id) REFERENCES magazines(magazine_id)
            );
        """)

        print("Tables created successfully")
    except sqlite3.Error as e:
        print("Error creating tables:", e)

def insert_publisher(conn, name):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO publishers (name) VALUES (?)", (name,))
        conn.commit()
    except sqlite3.Error as e:
        print("Error inserting publisher:", e)

def insert_magazine(conn, name, publisher_id):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO magazines (name, publisher_id) VALUES (?, ?)", (name, publisher_id))
        conn.commit()
    except sqlite3.Error as e:
        print("Error inserting magazine:", e)

def insert_subscriber(conn, name, address):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO subscribers (name, address) VALUES (?, ?)", (name, address))
        conn.commit()
    except sqlite3.Error as e:
        print("Error inserting subscriber:", e)

def insert_subscription(conn, subscriber_id, magazine_id, expiration_date):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date) 
            VALUES (?, ?, ?)
        """, (subscriber_id, magazine_id, expiration_date))
        conn.commit()
    except sqlite3.Error as e:
        print("Error inserting subscription:", e)

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        conn.execute("PRAGMA foreign_keys = 1")
        create_tables(conn)

        # Publishers
        insert_publisher(conn, "Tech World")
        insert_publisher(conn, "Health Daily")
        insert_publisher(conn, "Fashion Hub")

        # Magazines
        insert_magazine(conn, "Gadget Geek", 1)
        insert_magazine(conn, "Wellness Weekly", 2)
        insert_magazine(conn, "Style Star", 3)

        # Subscribers
        insert_subscriber(conn, "Alice", "123 Main St")
        insert_subscriber(conn, "Bob", "456 Oak Ave")
        insert_subscriber(conn, "Charlie", "789 Pine Rd")

        # Subscriptions
        insert_subscription(conn, 1, 1, "2025-12-31")
        insert_subscription(conn, 2, 2, "2025-11-30")
        insert_subscription(conn, 3, 3, "2025-10-15")

        conn.close()

def run_queries(conn):
    cursor = conn.cursor()

    print("\nAll subscribers:")
    for row in cursor.execute("SELECT * FROM subscribers"):
        print(row)

    print("\nMagazines sorted by name:")
    for row in cursor.execute("SELECT * FROM magazines ORDER BY name"):
        print(row)

    print("\nMagazines by publisher 'Tech World':")
    for row in cursor.execute("""
        SELECT m.name
        FROM magazines m
        JOIN publishers p ON m.publisher_id = p.publisher_id
        WHERE p.name = 'Tech World';
    """):
        print(row)

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        run_queries(conn)
        conn.close()

