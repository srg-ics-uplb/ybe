from flask import Flask, render_template, request
import random
import logging
from ybe import read_ybe_file
from ybe.lib.ybe_nodes import YbeExam

# Configure logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

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
    questions = load_and_shuffle_questions()
    return render_template('index.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    logger.debug(request.form)
    for question in questions:
        selected_options = request.form.getlist(f'question-{question["id"]}')
        if set(selected_options) == set(question['correct']):
            score += 1
    return render_template('result.html', score=score, total=len(questions))

if __name__ == '__main__':
    app.run(debug=True)
