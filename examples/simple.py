__author__ = 'Robbert Harms'
__date__ = '2020-04-07'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'GPL v3'


from ybe import read_ybe_file, YbeToLatex, YbeToMarkdown, YbeToDocx, YbeToODT, YbeToHTML

from importlib import resources
import random


ybe_exam = read_ybe_file('./simple.ybe')

#randomize questions
random.shuffle(ybe_exam.questions)

#randomize answers to questions
for question in ybe_exam.questions:
    random.shuffle(question.answers)


YbeToLatex().convert(ybe_exam, '/tmp/ybe/latex/main.tex', copy_resources=True)
YbeToMarkdown().convert(ybe_exam, '/tmp/ybe/markdown/main.md', copy_resources=True)
YbeToHTML().convert(ybe_exam, '/tmp/ybe/html/main.html', copy_resources=True)
YbeToDocx().convert(ybe_exam, '/tmp/ybe/main.docx')
YbeToODT().convert(ybe_exam, '/tmp/ybe/main.odt')
