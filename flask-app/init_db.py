import sqlite3
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    db_path = 'quiz.db'
    
    # Check if database exists
    db_exists = os.path.exists(db_path)
    
    # Connect (creates if not exists)
    conn = sqlite3.connect(db_path)
    
    if not db_exists:
        logger.info(f"Creating new database: {db_path}")
        # Create tables
        with open('schema.sql') as f:
            conn.executescript(f.read())
        logger.info("Database schema created successfully")
    else:
        logger.info(f"Database already exists: {db_path}")
    
    # Read and insert takers
    try:
        with open('takers.txt', 'r') as f:
            emails = [line.strip() for line in f if line.strip()]
            for email in emails:
                conn.execute('INSERT INTO user_sessions (email) VALUES (?)', (email,))
                logger.info(f"Added taker: {email}")
    except FileNotFoundError:
        logger.error("takers.txt not found")
        return
    
    conn.commit()
    conn.close()

init_db()