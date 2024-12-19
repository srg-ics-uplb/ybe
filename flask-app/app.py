from flask import Flask, render_template, request

app = Flask(__name__)

# Sample questions for the quiz
questions = [
    {
        'question': 'What is the capital of France?',
        'options': ['Berlin', 'Madrid', 'Paris', 'Lisbon'],
        'answer': 'Paris'
    },
    {
        'question': 'Which planet is known as the Red Planet?',
        'options': ['Earth', 'Mars', 'Jupiter', 'Saturn'],
        'answer': 'Mars'
    },
    {
        'question': 'What is the largest ocean on Earth?',
        'options': ['Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean', 'Pacific Ocean'],
        'answer': 'Pacific Ocean'
    }
]

@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    for i, question in enumerate(questions):
        selected_option = request.form.get(f'question-{i}')
        if selected_option == question['answer']:
            score += 1
    return render_template('result.html', score=score, total=len(questions))

if __name__ == '__main__':
    app.run(debug=True)
