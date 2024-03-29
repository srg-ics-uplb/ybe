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
pip3 install -r requirements.txt
make clean
make uninstall
make install
```

## Usage

Create the ybe file.

```yaml
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
