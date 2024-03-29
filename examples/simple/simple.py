
from ybe import read_ybe_file, YbeToLatex, YbeToMarkdown, YbeToDocx, YbeToODT, YbeToHTML

import random


ybe_exam = read_ybe_file('./simple.ybe')

#randomize questions
random.shuffle(ybe_exam.questions)

#randomize answers to questions
for question in ybe_exam.questions:
    random.shuffle(question.answers)

YbeToDocx().convert(ybe_exam, './simple.docx')
YbeToODT().convert(ybe_exam, './simple.odt')
