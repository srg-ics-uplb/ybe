<!-- {% if question.title is none %}
## Question {{ question_index }} (points: {{ question.points }})
{% else %}
## Question {{ question_index }}: {{ question.title.to_markdown() }} (points: {{ question.points }})
{% endif %}
{{ question.text.to_markdown() }}
-->

{% set choices = ['a','b','c','d','e','f','g','h'] %}

{{ question_index }} {{ question.text.to_markdown() }}

{% for answer in question.answers %}
{% if answer.correct is true %}
{{ choices[loop.index0] }}) *{{ answer.text.to_markdown() }}*
{% else %}
{{ choices[loop.index0] }}) {{ answer.text.to_markdown() }}
{% endif %}

{% endfor %}


