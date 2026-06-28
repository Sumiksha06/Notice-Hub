import sqlite3

DB_NAME = "project.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    
    # Create notices table with category
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        category TEXT NOT NULL DEFAULT 'General',
        created_by TEXT NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Migration: add category if it doesn't exist
    cursor.execute("PRAGMA table_info(notices)")
    cols = [col[1] for col in cursor.fetchall()]
    if "category" not in cols:
        cursor.execute("ALTER TABLE notices ADD COLUMN category TEXT DEFAULT 'General'")
    if "status" not in cols:
        cursor.execute("ALTER TABLE notices ADD COLUMN status TEXT DEFAULT 'new'")
    if "file_path" not in cols:
        cursor.execute("ALTER TABLE notices ADD COLUMN file_path TEXT")
    
    # Create notice_views table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notice_views (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        notice_id INTEGER NOT NULL,
        viewer_name TEXT NOT NULL,
        view_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (notice_id) REFERENCES notices(id)
    )
    """)

    # Create feedback table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        message TEXT NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create seen_notices table for user-specific tracking
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS seen_notices (
        user_id INTEGER NOT NULL,
        notice_id INTEGER NOT NULL,
        PRIMARY KEY (user_id, notice_id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (notice_id) REFERENCES notices(id)
    )
    """)
    
    conn.commit()
    conn.close()

def add_user(role, first_name, last_name, email, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO users (role, first_name, last_name, email, password)
        VALUES (?, ?, ?, ?, ?)
        """, (role, first_name, last_name, email, password))
        conn.commit()
        conn.close()
        return True, "Account Created Successfully!"
    except sqlite3.IntegrityError:
        return False, "Email already exists!"
    except Exception as e:
        return False, str(e)

def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def add_notice(title, content, category, admin_name, file_path=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notices (title, content, category, created_by, status, file_path) VALUES (?, ?, ?, ?, 'new', ?)", 
                   (title, content, category, admin_name, file_path))
    conn.commit()
    conn.close()

def mark_notice_as_seen(notice_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notices SET status='seen' WHERE id=?", (notice_id,))
    conn.commit()
    conn.close()

def mark_as_seen(user_id, notice_id):
    """Marks a notice as seen for a specific user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO seen_notices (user_id, notice_id) VALUES (?, ?)", (user_id, notice_id))
    conn.commit()
    conn.close()

def is_notice_seen(user_id, notice_id):
    """Checks if a notice has been seen by a specific user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM seen_notices WHERE user_id=? AND notice_id=?", (user_id, notice_id))
    seen = cursor.fetchone() is not None
    conn.close()
    return seen

def get_all_notices():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content, category, created_by, date, status, file_path FROM notices ORDER BY date DESC")
    notices = cursor.fetchall()
    conn.close()
    return notices

def get_notices_by_category(category):
    conn = get_connection()
    cursor = conn.cursor()
    if category == "All Notices":
        return get_all_notices()
    cursor.execute("SELECT id, title, content, category, created_by, date, status, file_path FROM notices WHERE category=? ORDER BY date DESC", (category,))
    notices = cursor.fetchall()
    conn.close()
    return notices

def get_notice_by_id(notice_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content, category, created_by, date, status, file_path FROM notices WHERE id=?", (notice_id,))
    notice = cursor.fetchone()
    conn.close()
    return notice

def delete_notice(notice_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notices WHERE id=?", (notice_id,))
    conn.commit()
    conn.close()

def update_notice(notice_id, title, content, category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notices SET title=?, content=?, category=? WHERE id=?", (title, content, category, notice_id))
    conn.commit()
    conn.close()

def add_view(notice_id, viewer_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notice_views (notice_id, viewer_name) VALUES (?, ?)", (notice_id, viewer_name))
    conn.commit()
    conn.close()

def get_views_for_notice(notice_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT viewer_name, view_date FROM notice_views WHERE notice_id=? ORDER BY view_date DESC", (notice_id,))
    views = cursor.fetchall()
    conn.close()
    return views

def add_feedback(name, role, message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (name, role, message) VALUES (?, ?, ?)", (name, role, message))
    conn.commit()
    conn.close()

def get_all_feedback():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback ORDER BY date DESC")
    feedbacks = cursor.fetchall()
    conn.close()
    return feedbacks

# Automatically initialize the database when this module is imported
initialize_db()

if __name__ == "__main__":
    print("Database initialized.")
