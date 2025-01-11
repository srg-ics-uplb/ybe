# YBE Web Quiz Application

A web-based quiz application that serves YBE format exams through a Flask interface.

## Features

- Loads questions from YBE (YAML-Based Exam) files
- Supports multiple choice and multiple response questions
- Markdown formatting for question text
- Image embedding support
- Answer randomization
- Points-based scoring system

## Installation

1. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Clone the repository
```bash
git clone https://github.com/srg-ics-uplb/ybe/
```

3. Build and install YBE

https://github.com/srg-ics-uplb/ybe/blob/master/README.md

4. Install dependencies

```bash
sudo apt install sqlite3
pip install flask markupsafe flask-markdown
```

IMPORTANT: There is a need to patch flask-markdown: `lib/python3.10/site-packages/flaskext/markdown.py`

Replace line 32:
`from flask import Markup`

with
`from markupsafe import Markup`

5. Create configuration file

Create a file named `config.py` in the flask-app directory:

```python
# filepath: flask-app/config.py
# Quiz configuration
EXAM_CODE = 'QUIZ1'               # Unique identifier for the quiz
MAX_LOGIN_ATTEMPTS = 3            # Maximum failed login attempts
YBE_FILE = 'questions.ybe'        # Path to YBE question file
QUIZ_TITLE = 'Sample Quiz'        # Title shown in browser
SCORES_PIN = '1234'              # PIN to access scores page

# Flask configuration
SECRET_KEY = 'your-secret-key'    # Required for session management
DEBUG = True                      # Enable debug mode
```

6. Run the application
```
cd flask-app
python app.py
```
## License

```
Copyright (C) 2024 JAC Hermocilla

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.
```

## Acknowledgement
Made with the assistance of GitHub Copilot