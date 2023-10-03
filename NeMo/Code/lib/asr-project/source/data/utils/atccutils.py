import logging
import string
from enum import Enum
from typing import *

__all__ = ["parse", "TerminalDirective"]


class TerminalDirective(Enum):
    """
    Enumeration of keys that are used in transcripts in Air-Traffic Control Complete. These
    are all the possible values that can occur as keys in the dictionaries returned by ``parse``.

    Each transcription is a list of lists (in Lisp syntax). The first value is a key which
    describes the type of data that occurs from the second value (on onward until the
    closing parenthetical).
    """

    #: indicates party sending the transmission e.g. (FROM AAABBBB)
    FROM = "FROM"
    #: indicates party receiving the transmission e.g. (TO AAABBBB)
    TO = "TO"
    #: text transcription of the transmission e.g. (TEXT ...)
    TEXT = "TEXT"
    #: start/end times of the transmission e.g. (TIMES start end)
    TIMES = "TIMES"
    #: comment(s) from transcriber e.g. (COMMENT "...")
    COMMENT = "COMMENT"
    #: metadata for the tape, also indicates that start of the tape e.g. (TAPE-HEADER "...")
    TAPE_HEADER = "TAPE-HEADER"
    #: meatdata for the tape, also indicates the end of the tape e.g. (TAPE-TAIL "...")
    TAPE_TAIL = "TAPE-TAIL"

    TRANSMISSION_ID = "NUM"
    """
    unspecified identifier included in some of the tapes, usualy a unique identifier
    based on the tape name, a dash, and a number representing the transmission
    i.e. 1 for the first transmission, 2 for the second, etc.
    """

    #: an escape sequence for contractions since the ' character has special meaning in LISP (denotes a list) e.g. (TEXT WE (QUOTE LL)) -> WE'LL
    QUOTE = "QUOTE"

    def __str__(self) -> str:
        return self.value


class TerminalConstant(Enum):
    """
    Enumeration of important constants used while parsing the Lisp files.
    """

    SPACE = " "
    OPEN_PAREN = "("
    CLOSE_PAREN = ")"

    def __str__(self) -> str:
        return self.value


class Directive(object):
    """
    Easier to use representation of transcript keys (referred to in this code as Directives).
    """

    def __init__(self, directive: str, arguments: str) -> "Directive":
        """
        :param directive: directive parsed from the current expression.
        :param arguments: arguments for the directive (or keys) from the current expression.
        """
        #: Parsed directive i.e. transcript key. Can correspond to any of the values enumerated in ``TerminalDirective``
        self.directive = TerminalDirective(directive)
        #: Arguments or values associated with the directive or key.
        self.arguments = arguments

    def __repr__(self) -> str:
        return f"Directive(directive={self.directive}, arguments='{self.arguments}')"


def get_string_and_normalize(string: str) -> str:
    """
    Normalize string, remove extra spaces and return.

    :param string: string to normalize
    :returns: Normalized string
    """
    if string is None:
        return ""

    string = string.replace("\n", " ")
    string = string.replace("\t", " ")
    string = string.strip()

    # these mongoloids wrote out contractions in AT LEAST 5 DIFFERENT WAYS
    # so here are special cases to normalize all of them (e.g. the contraction
    # for 'we will' ("we'll"), shows up as "we 'll", "we' ll", "we'll", "we ' ll", and "we (QUOTE ll)", wtf)
    #
    # according to the limited lexical analysis I've done on this data,
    # all 5 cases should be covered and normalized by this code
    while string.find("  ") != -1:
        string = string.replace("  ", " ")
    while string.find(" '") != -1:
        string = string.replace(" '", "'")
    while string.find("' ") != -1:
        string = string.replace("' ", "'")

    return string


def get_times(time_string: str) -> Dict[str, float]:
    """
    Extracts start and end times from a time field e.g. ``"TIME 12.34 45.56"`` start time would be
        12.34, end time would be 45.56.

    :param time_string: Time string from the ATCC transcript.
    :returns: A ``dict`` with keys for start and end times (values are ``float``s).
    """
    for char in string.whitespace:
        time_string = time_string.replace(char, " ")

    times = [x for x in time_string.strip().split(" ") if len(x) != 0]

    return {"start": float(times[0].strip()), "end": float(times[1].strip())}


DIRECTIVES = [str(val) for val in TerminalDirective.__members__.values()]
CONSTANT_TERMINALS = [str(val) for val in TerminalConstant.__members__.values()]

#: function callbacks for reformatting strings in the data i.e. transcript keys mapped to formatting functions.
callbacks: Dict[TerminalDirective, Callable] = {
    TerminalDirective.TEXT: get_string_and_normalize,
    TerminalDirective.TIMES: get_times,
}


def parse_directive(expression: str) -> Directive:
    """
    Parses a directive from an expression and returns a structured representation of it.

    :param expression: raw string to parse.
    :returns: Data representation of the directive. See ``Directive`` class for more info.
    """
    directive = ""
    arguments = ""
    position = 0

    while position < len(expression) and directive not in DIRECTIVES:
        directive += expression[position]
        position += 1

    if directive in DIRECTIVES and len(directive) != len(expression):
        arguments = expression[position:]

    return Directive(directive=directive, arguments=arguments.strip())


def parse_list(document: str, position: int) -> Tuple[int, List[str]]:
    """
    Parses and evaluates lisp lists from the document. This function is recursive and keeps track
        of its position in the document. The function recurses whenever an open parenthesis is found
        and returns when a closing parenthesis is found.

    :param document: document to parse i.e. collection of transcript samples (entire file as a string).
    :param position: current position in the document. Basically tracked by character because newlines
        are removed when the file is read into the program.
    :returns: a tuple containing the document position and parsed expressions e.g. (position, expressions)
    """
    lists: List[str] = []
    content = ""

    while document[position] != str(TerminalConstant.CLOSE_PAREN):
        current_char = document[position]

        # an expression starting and ending with quotes is to be taken as a string literal
        if current_char == '"':
            content += document[position]
            position += 1
            while document[position] != '"':
                content += document[position]
                position += 1

        if current_char == str(TerminalConstant.OPEN_PAREN):
            # lisp lists are defined recursively, so it makes sense to parse them recursively as well
            position, temp = parse_list(document, position + 1)

            # special case for escaped quotes in text fields
            try:
                parsed_expression = parse_directive(temp[0])
                if parsed_expression.directive == TerminalDirective.QUOTE:
                    content = content.strip() + "'" + parsed_expression.arguments
                else:
                    lists.extend(temp)
            except ValueError:
                # ValueError is raised if the keyword found doesn't match
                # any of the pre-defined keywords so we have to assume that
                # it is a mislabeled (or unlabeled) comment and does not
                # contribute significant information to the transcript
                logging.info(f"Discarding unrecognized symbol(s): {temp}")
        else:
            content += current_char
            position += 1

    if content != "":
        lists.append(content)

    return position + 1, lists


def reformat(data: List[str]) -> Dict:
    """
    Reformats and cleans up the data in the parased strings (or parses data from the string where
        necessary e.g. start/end time).

    :param data: list of strings to reformat.
    :returns: a ``dict`` with keys and values corresponding to directives and arguments parsed from
        the transcripts.
    """
    formatted_data = {}
    for expression in data:
        try:
            parsed_data = parse_directive(expression)
            callback_function = callbacks.get(
                parsed_data.directive, lambda x: x.strip()
            )
            formatted_data[str(parsed_data.directive)] = callback_function(
                parsed_data.arguments
            )
        except ValueError as e:
            logging.info(e)
        except Exception as e:
            logging.error(e)
    return formatted_data


def parse(lines: List[str]) -> List[Dict]:
    """
    Parse the given document and return a list of dictionaries with keys and values corresponding to data
    found in the transcripts/metadata.

    :param lines: list of lines in the document. These will be concatenated and parsed, with new line
        characters removed.
    :returns: ``list`` of ``dict`` objects with keys corresponding to transcript metadata keys (see
        ``TerminalDirective``) and values corresponding to actual metadata.

    Example of calling the ``parse`` function::

        import atccutils

        with open('transcript.txt', 'r', encoding='utf-8') as f:
            transcript_data = atccutils.parse(f.readlines())

    """
    document = ""
    for line in lines:
        # remove trailing whitespace
        document += line.rstrip()
    document_length = len(document)

    data_blocks = []
    position = 0
    while position < document_length:
        # start of a list
        if document[position] == str(TerminalConstant.OPEN_PAREN):
            position, block = parse_list(document, position + 1)
            data_blocks.append(block)
        else:
            position += 1

    for i, data in enumerate(data_blocks):
        data_blocks[i] = reformat(data)

    return data_blocks
