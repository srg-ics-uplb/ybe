from flask import Flask, render_template, request, redirect, url_for,session
from flask_session import Session
import random
import logging
from ybe import read_ybe_file
from ybe.lib.ybe_nodes import YbeExam
import uuid
import sqlite3
from config import EXAM_CODE, MAX_LOGIN_ATTEMPTS, YBE_FILE, QUIZ_TITLE
from datetime import datetime
from config import SCORES_PIN
from flaskext.markdown import Markdown

# Configure logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure key

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './sessions'

Markdown(app,output_format='html4')
Session(app)


def get_db():
    db = sqlite3.connect('quiz.db')
    db.row_factory = sqlite3.Row
    return db

def load_and_shuffle_questions():
    # Load YBE file
    ybe_data = read_ybe_file(YBE_FILE)

    questions = []
    
    # Shuffle questions
    random.shuffle(ybe_data.questions)
    for q in ybe_data.questions:
        # Get answers and shuffle them
        answers = q.answers.copy()
        random.shuffle(answers)
        
        # Move special answers to end
        for i, ans in enumerate(answers):
            if isinstance(ans.text.text, str):
                if "all of the above" in ans.text.text or "none of the above" in ans.text.text:
                    answers.append(answers.pop(i))
        
        # Format for template and log
        question_dict = {
            'id': q.id,
            'text': q.text.to_markdown(),
            'options': [a.text.text for a in answers],
            'correct': [a.text.text for a in answers if a.correct]
        }
        logger.debug(f"Converted question: {question_dict}")
        questions.append(question_dict)
    
    return questions

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        exam_code = request.form['exam_code']
        
        db = get_db()
        user = db.execute('SELECT * FROM user_sessions WHERE email = ?', (email,)).fetchone()
        
        if user:
            if exam_code == EXAM_CODE:
                # Check if there's an active session
                if user['session_id'] is not None:
                    logger.warning(f"Active session exists for {email}")
                    return render_template('login.html', 
                                    error='Another session is already active for this email',
                                    quiz_title=QUIZ_TITLE)
            


                # Create new session
                session['user_id'] = str(uuid.uuid4())
                session['email'] = email
                session['score'] = user['score']
                
                db.execute('''
                    UPDATE user_sessions 
                    SET session_id = ?, 
                        last_login_attempt = CURRENT_TIMESTAMP,
                        login_count = login_count + 1
                    WHERE email = ?
                ''', (session['user_id'], email))
                db.commit()

                if user['score'] > -1:
                    logger.info(f"User {email} already took quiz. Score: {user['score']}")
                    return render_template('result.html', 
                                    score=user['score'], 
                                    total=len(load_and_shuffle_questions()),
                                    completed=True)


                logger.info(f"New session created for {email}")
                return redirect(url_for('index'))
        
        return render_template('login.html', 
                             error='Invalid credentials',
                             quiz_title=QUIZ_TITLE)
                # Check if there's an active session
    
    return render_template('login.html', quiz_title=QUIZ_TITLE)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if session['score'] > -1:
        return render_template('result.html', 
                                score=session['score'], 
                                total=len(load_and_shuffle_questions()),
                                completed=True)

    if 'questions' not in session:
        questions = load_and_shuffle_questions()
        session['questions'] = questions
        logger.debug(f"User {session['user_id']}")
    
    questions = session['questions']
    return render_template('index.html', 
                         questions=questions,
                         quiz_title=QUIZ_TITLE)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    logger.info(session)
    if 'questions' in session and 'user_id' in session:
        db = get_db()
        try:
            for question in session['questions']:
                selected = request.form.getlist(f'question-{question["id"]}')
                if set(selected) == set(question['correct']):
                    score += 1
            
            total = len(session['questions'])
            logger.debug(f"User {session['user_id']}: Score {score}/{total}")
            
            # Update database
            db.execute('''
                UPDATE user_sessions 
                SET score = ?, 
                    submitted_at = CURRENT_TIMESTAMP,
                    completed_at = CURRENT_TIMESTAMP
                WHERE session_id = ?
            ''', (score, session['user_id']))
            db.commit()
            
            # Clear session
            #session.clear()
            
            session['score'] = score
            return render_template('result.html', score=score, total=total)
            
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            db.rollback()
            
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    if 'email' in session:
        db = get_db()
        try:
            db.execute('UPDATE user_sessions SET session_id = NULL WHERE email = ?', 
                      (session['email'],))
            db.commit()
            logger.info(f"Session cleared for {session['email']}")
        except sqlite3.Error as e:
            logger.error(f"Database error during logout: {e}")
            db.rollback()
    
    session.clear()
    return redirect(url_for('login'))

@app.route('/scores', methods=['GET', 'POST'])
def scores():
    if request.method == 'POST':
        if request.form.get('pin') == SCORES_PIN:
            db = get_db()
            scores = db.execute('''
                SELECT email, score, completed_at, created_at 
                FROM user_sessions 
                ORDER BY email ASC
            ''').fetchall()
            return render_template('scores.html',
                                authenticated=True,
                                scores=scores,
                                total_questions=len(load_and_shuffle_questions()),
                                quiz_title=QUIZ_TITLE)
        return render_template('scores.html', 
                             authenticated=False, 
                             error='Invalid PIN',
                             quiz_title=QUIZ_TITLE)
    return render_template('scores.html', 
                         authenticated=False,
                         quiz_title=QUIZ_TITLE)

if __name__ == '__main__':
    app.run(debug=True)
