from flask import Flask, render_template, request, session, redirect, url_for
import random
import logging
from ybe import read_ybe_file
from ybe.lib.ybe_nodes import YbeExam
import uuid
import sqlite3
from config import EXAM_CODE, MAX_LOGIN_ATTEMPTS, YBE_FILE
from datetime import datetime

# Configure logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure key

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
            'text': q.text.to_plaintext(),
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
        
        if user and exam_code == EXAM_CODE:
            if user['score'] > -1:  # Quiz already taken
                logger.info(f"User {email} already took quiz. Score: {user['score']}")
                return render_template('result.html', 
                                    score=user['score'], 
                                    total=len(load_and_shuffle_questions()),
                                    completed=True)
            
            session['user_id'] = str(uuid.uuid4())
            session['email'] = email
            db.execute('''
                UPDATE user_sessions 
                SET session_id = ?, 
                    last_login_attempt = CURRENT_TIMESTAMP,
                    login_count = login_count + 1
                WHERE email = ?
            ''', (session['user_id'], email))
            db.commit()
            return redirect(url_for('index'))
            
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if 'questions' not in session:
        questions = load_and_shuffle_questions()
        session['total_questions'] = len(questions)
        session['questions'] = questions
        logger.debug(f"User {session['user_id']}: Loaded {session['total_questions']} questions")
    return render_template('index.html', questions=session['questions'])

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    if 'questions' in session and 'user_id' in session:
        db = get_db()
        try:
            for question in session['questions']:
                selected = request.form.getlist(f'question-{question["id"]}')
                if set(selected) == set(question['correct']):
                    score += 1
            
            total = session.get('total_questions', 0)
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
            session.clear()
            
            return render_template('result.html', score=score, total=total)
            
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            db.rollback()
            
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
