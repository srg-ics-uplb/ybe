## Overview

This is a fork of [YAML Based Exams](https://github.com/robbert-harms/ybe) which 
allows users to create multiple choice exams/quizzes in yaml. The original package 
is no longer actively maintained so this fork was made. 

See the [original README](./README.rst).

## Installation

This assummes that you have a python3 environment with tools like pip3 installed.
Dev box is Ubuntu 22.04.

```bash
git clone https://github.com/srg-ics-uplb/ybe.git
cd ybe
sudo apt install -y pandoc
pip3 install -r requirements.txt
make clean
make uninstall
make install
```

## Usage

#### Create the ybe file

```yaml
# simple.ybe
ybe_version: 0.3.6

questions:
- multiple_choice:
   id: 2024_2nd
#   title: sample question
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
   id: 2024_2nd_1
#   title: sample question
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
```

#### Write the code

```python

from ybe import read_ybe_file, YbeToLatex, YbeToMarkdown, YbeToDocx, YbeToODT, YbeToHTML
import random

ybe_exam = read_ybe_file('./simple.ybe')

#randomize questions
random.shuffle(ybe_exam.questions)

#randomize answers to questions
for question in ybe_exam.questions:
    random.shuffle(question.answers)

#you can do more advanced stuff like filtering etc.
#by adding code. 

#Generate the documents which you can open in 
#MS Word or LibreOffice
YbeToDocx().convert(ybe_exam, './simple.docx')
YbeToODT().convert(ybe_exam, './simple.odt')

```


