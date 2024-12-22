from flask import Flask, render_template, request, session
import random
import logging
from ybe import read_ybe_file
from ybe.lib.ybe_nodes import YbeExam
import uuid

# Configure logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure key

def load_and_shuffle_questions():
    # Load YBE file
    ybe_data = read_ybe_file("example.ybe")

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
                if "All of the above" in ans.text.text or "None of the above" in ans.text.text:
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

@app.route('/')
def index():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    if 'questions' not in session:
        questions = load_and_shuffle_questions()
        session['total_questions'] = len(questions)
        session['questions'] = questions
        logger.debug(f"User {session['user_id']}: Loaded {session['total_questions']} questions")
    return render_template('index.html', questions=session['questions'])

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    if 'questions' in session:
        for question in session['questions']:
            selected = request.form.getlist(f'question-{question["id"]}')
            if set(selected) == set(question['correct']):
                score += 1
        total = session.get('total_questions', 0)
        logger.debug(f"User {session['user_id']}: Score {score}/{total}")
        session.pop('questions', None)
        return render_template('result.html', score=score, total=total)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
