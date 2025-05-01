import sqlite3
import os
from datetime import datetime, timedelta

# Define database path and ensure directory exists
db_path = "./db/magazines.db"
os.makedirs(os.path.dirname(db_path), exist_ok=True)

def create_connection():
    """Create and return a database connection with foreign keys enabled"""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn  


def add_publisher(conn, name):
    """Add a publisher if it doesn't already exist"""
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO publishers (name) VALUES (?)", (name,))
        if cursor.rowcount > 0:
            print(f"✅ Added publisher: {name}")
            return cursor.lastrowid
        else:
            print(f"⏩ Publisher already exists: {name}")
            # Return existing publisher's ID
            cursor.execute("SELECT id FROM publishers WHERE name = ?", (name,))
            return cursor.fetchone()[0]
    except sqlite3.Error as e:
        print(f"❌ Error adding publisher {name}: {e}")
        return None
    

def add_magazine(conn, name, publisher_id):
    """Add a magazine if it doesn't already exist"""
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO magazines (name, publisher_id) VALUES (?, ?)", 
                     (name, publisher_id))
        if cursor.rowcount > 0:
            print(f"✅ Added magazine: {name}")
            return cursor.lastrowid 
        else:
            print(f"⏩ Magazine already exists: {name}")
            # Return existing magazine's ID
            cursor.execute("SELECT id FROM magazines WHERE name = ?", (name,))
            return cursor.fetchone()[0]
    except sqlite3.Error as e:
        print(f"❌ Error adding magazine {name}: {e}")
        return None

def add_subscriber(conn, name, address):
    """Add a subscriber if the name+address combination doesn't exist"""
    try:
        cursor = conn.cursor()
        # Check if subscriber with same name AND address exists
        cursor.execute("SELECT id FROM subscribers WHERE name = ? AND address = ?", 
                      (name, address))
        existing = cursor.fetchone()
        
        if existing:
            print(f"⏩ Subscriber already exists: {name} at {address}")
            return existing[0]
        else:
            cursor.execute("INSERT INTO subscribers (name, address) VALUES (?, ?)", 
                          (name, address))
            print(f"✅ Added subscriber: {name}")
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"❌ Error adding subscriber {name}: {e}")
        return None


def add_subscription(conn, subscriber_id, magazine_id, expiration_date):
    """Add a subscription if it doesn't already exist"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO subscriptions 
            (subscriber_id, magazine_id, expiration_date) 
            VALUES (?, ?, ?)
        """, (subscriber_id, magazine_id, expiration_date))
        
        if cursor.rowcount > 0:
            print(f"✅ Added subscription: subscriber {subscriber_id} to magazine {magazine_id}")
            return True
        else:
            print(f"⏩ Subscription already exists: subscriber {subscriber_id} to magazine {magazine_id}")
            return False
    except sqlite3.Error as e:
        print(f"❌ Error adding subscription: {e}")
        return False

def create_tables(conn):
    """Create all tables with proper constraints"""
    try:
        cursor = conn.cursor()

        # Create publishers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS publishers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
        """)

       # Create magazines table with foreign key to publishers
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                publisher_id INTEGER NOT NULL,
                FOREIGN KEY (publisher_id) REFERENCES publishers(id) ON DELETE CASCADE
            );
        """)

        # Create subscribers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL
            );
        """)

        # Create subscriptions join table with foreign keys
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscriber_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                expiration_date TEXT NOT NULL,
                FOREIGN KEY (subscriber_id) REFERENCES subscribers(id) ON DELETE CASCADE,
                FOREIGN KEY (magazine_id) REFERENCES magazines(id) ON DELETE CASCADE,
                UNIQUE(subscriber_id, magazine_id)  -- Prevent duplicate subscriptions
            );
        """)

        conn.commit()
        print("✅ All tables created successfully with proper constraints")
        return True
    except sqlite3.Error as e:
        print(f"❌ Error creating tables: {e}")
        return False



def populate_sample_data(conn):
    """Populate all tables with sample data"""
    # Add publishers
    pub1 = add_publisher(conn, "Science Publications")
    pub2 = add_publisher(conn, "Tech Media Inc.")
    pub3 = add_publisher(conn, "Nature Press")
    add_publisher(conn, "Science Publications")  
    
    # Add magazines
    mag1 = add_magazine(conn, "Quantum Physics", pub1)
    mag2 = add_magazine(conn, "AI Today", pub2)
    mag3 = add_magazine(conn, "Wildlife Journal", pub3)
    add_magazine(conn, "AI Today", pub2)  
    
    # Add subscribers
    sub1 = add_subscriber(conn, "Alice Johnson", "123 Science St")
    sub2 = add_subscriber(conn, "Bob Smith", "456 Tech Ave")
    sub3 = add_subscriber(conn, "Alice Johnson", "789 Nature Rd")  # Same name, different address
    add_subscriber(conn, "Alice Johnson", "123 Science St")  # Should show already exist

    # Add subscriptions (expiring 1 year from today)
    today = datetime.now().strftime("%Y-%m-%d")
    next_year = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    
    add_subscription(conn, sub1, mag1, next_year)
    add_subscription(conn, sub2, mag2, next_year)
    add_subscription(conn, sub3, mag3, next_year)
    add_subscription(conn, sub1, mag1, next_year)  # Should show already exists


def main():
    try:
        conn = create_connection()
        
        # Create tables 
        if not create_tables(conn):
            return
        
        # Populate with sample data
        populate_sample_data(conn)
        conn.commit()
        print("\n✅ Database setup and population complete!")
        
        # Execute the required queries
        print("\n" + "="*50)
        print("QUERY RESULTS")
        print("="*50)
        
        # Query 1: All subscribers
        print("\n1. All subscribers:")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subscribers")
        for row in cursor.fetchall():
            print(f"ID: {row[0]}, Name: {row[1]}, Address: {row[2]}")
        
        # Query 2: All magazines sorted by name
        print("\n2. All magazines sorted by name:")
        cursor.execute("SELECT * FROM magazines ORDER BY name")
        for row in cursor.fetchall():
            print(f"ID: {row[0]}, Name: {row[1]}, Publisher ID: {row[2]}")

        # Query 3: Magazines for 'Science Publications' publisher
        print("\n3. Magazines published by 'Science Publications':")
        cursor.execute("""
            SELECT m.id, m.name 
            FROM magazines m
            JOIN publishers p ON m.publisher_id = p.id
            WHERE p.name = 'Science Publications'
        """)
        for row in cursor.fetchall():
            print(f"ID: {row[0]}, Name: {row[1]}")


        # # Verification queries
        # print("\nCurrent data:")
        # for table in ["publishers", "magazines", "subscribers", "subscriptions"]:
        #     print(f"\n{table.upper()}:")
        #     cursor = conn.cursor()
        #     cursor.execute(f"SELECT * FROM {table}")
        #     for row in cursor.fetchall():
        #         print(row)
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()

# if db_dir:  
#     os.makedirs(db_dir, exist_ok=True)

# try:
#     # Connect to database (this will create it if it doesn't exist)
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     # Enable foreign key constraints
#     conn.execute("PRAGMA foreign_keys = ON")

#     # Create publishers table
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS publishers (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT UNIQUE NOT NULL
#         );
#     """)

#     # Create magazines table with foreign key to publishers
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS magazines (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT UNIQUE NOT NULL,
#             publisher_id INTEGER NOT NULL,
#             FOREIGN KEY (publisher_id) REFERENCES publishers(id) ON DELETE CASCADE
#         );
#     """)

#     # Create subscribers table
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS subscribers (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             address TEXT NOT NULL
#         );
#     """)

#     # Create subscriptions join table with foreign keys
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS subscriptions (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             subscriber_id INTEGER NOT NULL,
#             magazine_id INTEGER NOT NULL,
#             expiration_date TEXT NOT NULL,
#             FOREIGN KEY (subscriber_id) REFERENCES subscribers(id) ON DELETE CASCADE,
#             FOREIGN KEY (magazine_id) REFERENCES magazines(id) ON DELETE CASCADE,
#             UNIQUE(subscriber_id, magazine_id)  -- Prevent duplicate subscriptions
#         );
#     """)

#     # Commit 
#     conn.commit()
#     print("✅ All tables created successfully with proper constraints")

#     # Verify 
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     print("\nTables in database:")
#     for table in cursor.fetchall():
#         print(f"- {table[0]}")
#         # Show table structure
#         cursor.execute(f"PRAGMA table_info({table[0]});")
#         print("  Columns:")
#         for col in cursor.fetchall():
#             print(f"    {col[1]:<15} {col[2]:<10} {'PK' if col[5] else ''} {'NOT NULL' if col[3] else ''}")

# except sqlite3.Error as e:
#     print(f"❌ Error creating tables: {e}")

# finally:
#     if conn:
#         conn.close()

