## Overview

This is a fork of [YAML Based Exams](https://github.com/robbert-harms/ybe) which 
allows users to create multiple choice exams/quizzes in yaml. The original package 
seems to be unmaintained so this fork was made. 

See the [original README](./README.rst) for more advanced usage.

## Installation

This assummes that you have a python3 environment with tools like pip3 installed.
Dev box used is Ubuntu 22.04. The repo also works in GitHub's Codespaces in case 
you don't have a local enviroment setup.

```bash
git clone https://github.com/srg-ics-uplb/ybe.git
cd ybe
sudo apt install -y build-essential pandoc
pip3 install -r requirements.txt wheel
make clean
make uninstall
make install
```

## Usage

#### Create the ybe file

```yaml
ybe_version: 0.3.6

#simple.ybe

questions:
- multiple_choice:
   id: q1
   points: 1
   text: Which of the following devices is responsible for selecting the best path for a datagram?
   answers:
      - answer:
         text: NIC
      - answer:
         text: Hub
      - answer:
         text: Switch
      - answer: 
         text: Router
         correct: true

- multiple_choice:
   id: q2
   points: 1
   text: Which of the following protocols use distance-vector routing?
   answers:
      - answer:
         text: OSPF
      - answer:
         text: RIP
         correct: true
      - answer:
         text: BGP
      - answer: 
         text: DHCP
 
- multiple_response:
   id: q3
   points: 1
   text: A socket is composed of?
   answers:
      - answer:
         text: URL
      - answer:
         text: IP Address
         correct: true
      - answer:
         text: MAC Address
      - answer: 
         text: Port Number
         correct: true

```

#### Write the code

```python
#simple.py

from ybe import read_ybe_file, YbeToLatex, YbeToMarkdown, YbeToDocx, YbeToODT, YbeToHTML
import random

ybe_exam = read_ybe_file('./simple.ybe')

#randomize questions
random.shuffle(ybe_exam.questions)

#randomize answers to questions
for question in ybe_exam.questions:
    random.shuffle(question.answers)

#you can do more advanced stuff like filtering etc.
#by adding the necessary code. 

#Generate the documents which you can open in 
#MS Word or LibreOffice
YbeToDocx().convert(ybe_exam, './simple.docx')
YbeToODT().convert(ybe_exam, './simple.odt')

```

#### Run the code

```bash
python3 ./simple.py
```
