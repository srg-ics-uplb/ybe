import sqlite3
import logging
import os
import shutil
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def logout_users(email):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    try:
        if email == 'all':
            active = cursor.execute(
                'SELECT COUNT(*) FROM user_sessions WHERE session_id IS NOT NULL'
            ).fetchone()[0]
            cursor.execute('UPDATE user_sessions SET session_id = NULL')
            logger.info(f"Logged out {active} active users")
        else:
            cursor.execute(
                'UPDATE user_sessions SET session_id = NULL WHERE email = ?',
                (email,)
            )
            if cursor.rowcount > 0:
                logger.info(f"Logged out user: {email}")
            else:
                logger.error(f"User not found or already logged out: {email}")
                return

        # Clear session files
        sessions_dir = 'session'
        if os.path.exists(sessions_dir):
            shutil.rmtree(sessions_dir)
            os.makedirs(sessions_dir)
            logger.info(f"Cleared {sessions_dir} directory")

        conn.commit()

    except Exception as e:
        logger.error(f"Error during logout: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Logout quiz users')
    parser.add_argument(
        'email', help='Email to logout (use "all" for all users)')
    args = parser.parse_args()

    logout_users(args.email)
