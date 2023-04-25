import re # to be used: logging, sys

# INCOMPLETE! (KINDA) ALSO VERY MESSY, SORRY ABOUT THAT.

class LexingError(Exception):

    def __init__(self, message: str):

        self.message = message
        super().__init__(self.message)

    def __traceback__(self):
        pass


class REPatterns():

    def __init__(self, *args: tuple):

        self.match_patterns = self.__stuff__(args)
        self.compiled_pattern = re.compile(self.match_patterns)

    def __stuff__(self, _set_list: list) -> str:

        _master_list = []
        _prev = None

        for _pattern_set in _set_list:

            if _prev == None:
                _prev = _pattern_set

            else:   
                _master_list = _prev + _pattern_set # add 
                _prev = _master_list
            
        return '|'.join('(?P<%s>%s)' % _set for _set in _master_list)
    
# TO BE REMOVED AND REPLACED WITH CONFIG PATTERNS -- FOR TESTING PURPOSES CURRENTLY:

literals = [

    ('INTEGER', r'[0-9]+'),
    ('FLOAT', r'[0-9]*\.[0-9]+'),
    ('STRING', r'\"(\\.|[^\\"])*\"'),
    ('BOOLEAN', r'(True|False)'), 
    ('BYTE', r'0x[0-9a-fA-F]{2}'),
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),

] 

kw_patterns = [

    ('IF', r'\bif\b'), # if
    ('ELSE', r'\belse\b'), # else
    ('ELIF', r'\belse\s+if\b'), # elif
    ('FOR', r'\bfor\b'), # for
    ('WHILE', r'\bwhile\b'), # while
    ('TRY', r'\btry\b'), # try
    ('EXCEPT', r'\bcatch\b'), # except
    ('FINALLY', r'\blast\b'), # finally
    ('RAISE', r'\btoss\b'), # raise
    ('FUNCTION', r'\bfunc\b'), # def
    ('RETURN', r'\breturn\b'), # return
    ('YIELD', r'\byield\b'), # yield
    ('BREAK', r'\bexit\b'), # break
    ('IMPORT', r'\busing\b'), # import
    ('FROM', r'\bfrom\b'), # from
    ('AS', r'\bas\b'), # as
    ('WITH', r'\bwith\b'), # with
    ('AND', r'\band\b'), # and
    ('OR', r'\bor\b'), # or,
    ('NOT', r'\bnot\b'), # not,
    ('IS', r'\bis\b'), # is,
    ('CONTINUE', r'\bskip\s'), # continue
    ('PASS', r'\bpass\s'), # pass
    ('CLASS', r'\bclass\b'), # class
    ('ASSERT', r'\bverify\b'), # assert
    ('NONE', r'\bNull\b'), # None
    ('LAMBDA', r'\blambda\b'), # lambda
    ('NONLOCAL', r'\bforeign\b'), # nonlocal
    ('GLOBAL', r'\bglobal\b'), # global
    ('PRINT', r'\bout\b')

]

oper_patterns = [ 

    ('PLUS_EQUAL', r'\+='),
    ('MINUS_EQUAL', r'-='),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MULTIPLY', r'\*'),    
    ('EXPONENT', r'\*\*(?!\*)'),
    ('INT_DIVISION', r'/{2}'),
    ('FLOAT_DIVISION', r'/'),
    ('MODULO', r'\%'),
    ('EQUAL_TO', r'={2}'),
    ('ASSIGN', r'='),

]

delim_patterns = [

    ('LEFT_PARENTH', r'\('),
    ('RIGHT_PARENTH', r'\)'),
    ('LEFT_BRACKET', r'\['),
    ('RIGHT_BRACKET', r'\]'),
    ('LEFT_CURLY_BRACKET', r'\{'),
    ('RIGHT_CURLY_BRACKET', r'\}'),

]

boolean_oper_patterns = [

    ('LESS_THAN', r'\b<\b'),
    ('GREATER_THAN', r'\b>\b'),
    ('LESS_THAN_EQUAL_TO', r'\b<=\b'),
    ('GREATER_THAN_EQUAL_TO', r'\b>=\b'),
    ('NOT_EQUAL', r'\b!=\b'),

]

invalid_patterns = [

    ('INVALID', r'@|`|;|&|\\')

]

misc_patterns = [

    ('POUND', r'#'),
    ('TAB', r'^\s+\b|\\t'),
    ('WHITESPACE', r'\s'), 
    ('EMPTY', r'^\\n$'),
    ('NEWLINE', r'\\n|\\r|\\r\\n'),

]

class Token():
    """ Base class for lexed and labelled tokens. """

    def __init__(self, _token: tuple[2], _location: tuple, _unique_id: int):

        _location = iter(_location) 
        _token = iter(_token)

        self.raw, self.type = next(_token), next(_token)
        self.row, self.column = next(_location), next(_location) 
        self.id = _unique_id

    def __str__(self) -> str:

        """ 
        String representation of a Token object. 

        Output: ' token: < token.id > | raw: < token.raw > | type: < token.type > '
        
        """

        return (f'token: < {self.id} > | raw: < {self.raw} > | type: < {self.type} >')
        
           
class Lexer():
    """ Base class for LB interpreter lexer/tokenizer. """

    def __init__(self, *args: list):

        patterns = [arg for arg in args] #<-- TO BE EXPANDED
        self.re_patterns = REPatterns(kw_patterns, literals, delim_patterns, boolean_oper_patterns, oper_patterns, misc_patterns, invalid_patterns,) # NEEDS CHANGING ... very long
        self.identifier_cache = {} # to hold the program's identifier tokens (used to distinguish references vs. declarations)
        self.unique_id = self.identifier_id = 1
        self.curr_line = 0


    def __tokenize__(self, _line: str) -> Token: # token generator for each line
        """ Generator that finds regular expression pattern matches (tokens) in a line. """

        self.line_is_comment_body = False # reset line_is_comment_body at the start of a new line

        _curr_row = self.curr_line + 1
        _line_contents = _line.encode('unicode-escape').decode() # preserve newline chars, etc.
        
        for m in re.finditer(self.re_patterns.compiled_pattern, _line_contents): # for each token that matches a given pattern...

            _group = self.__group__(m)
            _token_type = next(_group)
            _token_value = next(_group)

            _curr_column = _line_contents.find(_token_value) + 1
            _temp_token = self.__proof__(Token((_token_value, _token_type), (_curr_row, _curr_column), self.unique_id))
           
            if _temp_token is None: # ignore newline characters (code apt to change)
                continue
            else:
                yield _temp_token

                _whitespace = ' ' * len(_token_value)
                _line_contents = _line_contents.replace(_token_value, _whitespace, 1) # remove token from input string to avoid any lexer confusion with seeking methods
                self.unique_id += 1

        self.curr_line += 1
        

    def __group__(self, _match): # return the named group "members", first and last 

        if self.line_is_comment_body:
            yield "COMMENT_BODY"
        else:
            yield _match.lastgroup

        yield _match.group()


    def __proof__(self, _token: Token) -> Token: # Semi WIP

        if _token.type == 'INVALID':
            raise LexingError(f"Invalid character '{_token.raw}' in expression.")

        elif _token.type == "POUND":
            self.line_is_comment_body = True

        elif _token.type == "NEWLINE":
            return None

        elif _token.type == "IDENTIFIER": # if the identifier doesn't exist, add it to the identifier cache and advance

            if _token.raw not in self.identifier_cache:

                self.identifier_cache[_token.raw] = {
                    "IDENTIFIER": self.identifier_id,
                    "CALLABLETYP": None,
                    "REFERENCES": { 0: _token.id },
                }

                self.identifier_id += 1

            else: # if the identifier already exists, this token is a reference of that object.

                _token.type = "REFERENCE"
                _access = self.identifier_cache[_token.raw]["REFERENCES"]
                _access[len(_access)] = _token.id # insert the reference into the reference list

        else:
            pass

        return _token


    def lex(self, _lines: list[str]) -> list[Token]:

        if not isinstance(_lines, list): 
            raise LexingError(fr"Argument must be type 'list' containing input lines.")

        elif not _lines:
            self.lex_list = []

        else:
            self.lex_list = list(self.__tokenize__(_line) for _line in _lines)
