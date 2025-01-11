import sqlite3
import os
import logging
import string
import random
import csv

def generate_exam_code():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(5))

def init_db():
    db_path = 'quiz.db'
    logger = logging.getLogger(__name__)
    
    # Check if database exists
    db_exists = os.path.exists(db_path)
    
    # Connect (creates if not exists)
    conn = sqlite3.connect(db_path)
    
    if not db_exists:
        logger.info(f"Creating new database: {db_path}")
        with open('schema.sql') as f:
            conn.executescript(f.read())
        logger.info("Database schema created successfully")
    else:
        logger.info(f"Database already exists: {db_path}")
    
    # Generate codes and save to CSV
    quiz_codes = {}
    try:
        with open('takers.txt', 'r') as f:
            emails = [line.strip() for line in f if line.strip()]
            
            # Generate unique codes
            for email in emails:
                while True:
                    code = generate_exam_code()
                    if code not in quiz_codes.values():
                        quiz_codes[email] = code
                        break
            
            # Save to CSV
            with open('quiz_codes.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['email', 'quiz code'])
                for email, code in quiz_codes.items():
                    writer.writerow([email, code])
            
            # Insert into database
            for email, code in quiz_codes.items():
                conn.execute(
                    'INSERT INTO user_sessions (email, quiz_code, score) VALUES (?, ?, -1)',
                    (email, code)
                )
                logger.info(f"Added taker: {email} with code: {code}")
                
    except FileNotFoundError:
        logger.error("takers.txt not found")
        return
    
    conn.commit()
    conn.close()

init_db()