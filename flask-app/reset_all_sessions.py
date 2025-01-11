import sqlite3
import os
import logging
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def reset_sessions():
    # Connect to database
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    
    try:
        # Reset session IDs in database
        cursor.execute('UPDATE user_sessions SET session_id = NULL')
        logger.info("Reset all session IDs in database")
        
        # Delete session files
        sessions_dir = 'flask_session'
        if os.path.exists(sessions_dir):
            shutil.rmtree(sessions_dir)
            os.makedirs(sessions_dir)
            logger.info(f"Cleared {sessions_dir} directory")
        
        # Commit changes
        conn.commit()
        logger.info("Successfully reset all sessions")
        
    except Exception as e:
        logger.error(f"Error resetting sessions: {e}")
        conn.rollback()
    finally:
        conn.close()

reset_sessions()