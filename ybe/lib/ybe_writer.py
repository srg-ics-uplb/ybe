__author__ = 'Robbert Harms'
__date__ = '2020-04-16'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'GPL v3'

from io import StringIO
from ruamel.yaml import YAML
from ruamel.yaml import scalarstring
from ruamel.yaml.comments import CommentedSeq

from ybe.__version__ import __version__
from ybe.lib.errors import YbeVisitingError
from ybe.lib.ybe_contents import YbeNodeVisitor


def write_ybe_string(ybe_file, minimal=False):
    """Dump the provided YbeFile as a .ybe formatted string.

    Args:
        ybe_file (ybe.lib.ybe_contents.YbeFile): the ybe file contents to dump
        minimal (boolean): if set to True we only print the configured options.
            By default this flag is False, meaning we print all the available options, if needed with null placeholders.

    Returns:
        str: an .ybe (Yaml) formatted string
    """
    visitor = YbeConversionVisitor(minimal=minimal)
    content = visitor.visit(ybe_file)

    yaml = YAML(typ='rt')
    yaml.default_flow_style = False
    yaml.allow_unicode = True
    yaml.indent(mapping=4, offset=4, sequence=4)

    def beautify_line_spacings(s):
        ret_val = ''
        previous_new_line = ''
        in_questions_block = False
        for line in s.splitlines(True):
            new_line = line

            if in_questions_block:
                if line.startswith('    '):
                    new_line = line[4:]
                elif line.startswith('\n'):
                    pass
                else:
                    in_questions_block = False
            else:
                if line.startswith('questions:'):
                    in_questions_block = True

            if any(new_line.startswith(el) for el in ['info', 'questions:', '- multiple_choice:', '- open:'])\
                    and not previous_new_line.startswith('\nquestions:'):
                new_line = '\n' + new_line

            previous_new_line = new_line
            ret_val += new_line
        return ret_val

    yaml.dump(content, result := StringIO(), transform=beautify_line_spacings)
    return result.getvalue()


class YbeConversionVisitor(YbeNodeVisitor):

    def __init__(self, minimal=False):
        """Converts an YbeFile into a Python dictionary.

        Args:
            minimal (boolean): if set to True we only print the configured options.
                By default this flag is False, meaning we print all the available options, if needed with null placeholders.
        """
        self.minimal = minimal

    def visit(self, node):
        method = f'_visit_{node.__class__.__name__}'
        if not hasattr(self, method):
            raise YbeVisitingError(f'Unknown node encountered of type {type(node)}.')
        return getattr(self, method)(node)

    def _visit_YbeFile(self, node):
        content = {'ybe_version': __version__}

        if len(info := self.visit(node.file_info)) or not self.minimal:
            content['info'] = info

        content['questions'] = [self.visit(question) for question in node.questions]
        return content

    def _visit_YbeFileInfo(self, node):
        info = {}

        for item in ['title', 'description', 'document_version', 'creation_date']:
            if (value := getattr(node, item)) is not None or not self.minimal:
                info[item] = value

        if len(value := node.authors) or not self.minimal:
            info['authors'] = value

        return info

    def _visit_MultipleChoice(self, node):
        """Convert the given :class:`ybe.lib.ybe_contents.MultipleChoice` into a dictionary.

        Args:
            node (ybe.lib.ybe_contents.MultipleChoice): the question to convert

        Returns:
            dict: the question as a dictionary
        """
        data = {'id': node.id}
        data.update(self.visit(node.text))
        data['answers'] = [{'answer': self.visit(el)} for el in node.answers]

        if len(meta_data := self.visit(node.meta_data)) or not self.minimal:
            data['meta_data'] = meta_data

        return {'multiple_choice': data}

    def _visit_OpenQuestion(self, node):
        """Convert the given :class:`ybe.lib.ybe_contents.OpenQuestion` into a dictionary.

        Args:
            node (ybe.lib.ybe_contents.OpenQuestion): the question to convert

        Returns:
            dict: the question as a dictionary
        """
        data = {'id': node.id}
        data.update(self.visit(node.text))

        if len(options := self.visit(node.options)) or not self.minimal:
            data['options'] = options

        if len(meta_data := self.visit(node.meta_data)) or not self.minimal:
            data['meta_data'] = meta_data

        return {'open': data}

    def _visit_Text(self, node):
        return {'text': self._yaml_format_text(node.text)}

    def _visit_TextLatex(self, node):
        return {'text_latex': self._yaml_format_text(node.text)}

    def _visit_MultipleChoiceAnswer(self, node):
        """Convert a single multiple choice answer

        Args:
            node (ybe.lib.ybe_contents.MultipleChoiceAnswer): the multiple choice answers to convert to text.

        Returns:
            dict: the converted answer
        """
        data = {}
        data.update(self.visit(node.text))
        data['points'] = node.points
        if node.correct:
            data['correct'] = node.correct
        return data

    def _visit_OpenQuestionOptions(self, node):
        if self.minimal:
            return {k: v for k, v in node.__dict__.items() if v is not None}
        return node.__dict__

    def _visit_QuestionMetaData(self, node):
        """Convert the meta data object into a dictionary.

        Args:
            node (ybe.lib.ybe_contents.QuestionMetaData): the text object to convert to a dict text element

        Returns:
            dict: the converted node
        """
        result = {}

        if len(general := self.visit(node.general)) or not self.minimal:
            result['general'] = general

        if len(lifecycle := self.visit(node.lifecycle)) or not self.minimal:
            result['lifecycle'] = lifecycle

        if len(classification := self.visit(node.classification)) or not self.minimal:
            result['classification'] = classification

        if len(analytics := self.visit(node.analytics)) or not self.minimal:
            result['analytics'] = analytics

        return result

    def _visit_GeneralQuestionMetaData(self, node):
        data = node.__dict__
        data['keywords'] = self._yaml_inline_list(data['keywords'])

        if self.minimal:
            minimal_data = {k: v for k, v in data.items() if v is not None}

            if not len(data['keywords']):
                del minimal_data['keywords']
            return minimal_data

        return data

    def _visit_AnalyticsQuestionMetaData(self, node):
        return node.analytics

    def _visit_ClassificationQuestionMetaData(self, node):
        data = node.__dict__
        data['related_concepts'] = self._yaml_inline_list(data['related_concepts'])

        if self.minimal:
            minimal_data = {k: v for k, v in data.items() if v is not None}

            if not len(data['related_concepts']):
                del minimal_data['related_concepts']
            return minimal_data

        return data

    def _visit_LifecycleQuestionMetaData(self, node):
        data = node.__dict__
        if self.minimal:
            return {k: v for k, v in data.items() if v is not None}
        return node.__dict__

    @staticmethod
    def _yaml_format_text(text):
        if '\n' in text:
            return scalarstring.PreservedScalarString(text)
        return text

    @staticmethod
    def _yaml_inline_list(l):
        """Return a list wrapped in a ruamal yaml block, such that the list will be displayed inline.

        Args:
            l (list): the list to wrap

        Returns:
            CommentedSeq: the commented list with the flow style set to True
        """
        wrapped = CommentedSeq(l)
        wrapped.fa.set_flow_style()
        return wrapped
