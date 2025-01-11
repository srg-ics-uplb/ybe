import sqlite3
import logging
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def reset_score(email):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    try:
        if email == 'all':
            cursor.execute('''
                UPDATE user_sessions 
                SET score = -1,
                    session_id = NULL,
                    completed_at = NULL
            ''')
            logger.info("Reset all scores to -1")
        else:
            cursor.execute('''
                UPDATE user_sessions 
                SET score = -1,
                    session_id = NULL,
                    completed_at = NULL
                WHERE email = ?
            ''', (email,))
            if cursor.rowcount > 0:
                logger.info(f"Reset score for {email}")
            else:
                logger.error(f"Email not found: {email}")

        conn.commit()

    except Exception as e:
        logger.error(f"Error resetting score: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reset quiz scores')
    parser.add_argument('email', help='Email address to reset (use "all" for all users)')
    args = parser.parse_args()
    
    reset_score(args.email)