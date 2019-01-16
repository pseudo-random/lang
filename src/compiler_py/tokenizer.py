# MIT License
#
# Copyright (c) 2018 - 2019 pseudo-random <josh.leh.2018@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys, utils
from consts import *

class token:
    def __init__ (self, token_type, value, line):
        self.type = token_type
        self.value = value
        self.line = line

def get_token_type (name):
    if utils.is_bool (name):
        return TOKEN_VALUE_BOOL
    elif utils.is_int (name) or utils.is_hex (name):
        return TOKEN_VALUE_INT
    elif utils.is_float (name):
        return TOKEN_VALUE_FLOAT

    return TOKEN_NAME

def print_tokens (tokens):
    print ("Type\tValue")

    for token in tokens:
        print (token_names[token.type] + "\t" + token.value)

def tokenize (code):
    name = ""
    is_str = False
    is_comment = False
    ignore_newline = False
    line = 1

    tokens = []

    it = 0
    while it < len (code):
        char = code [it]
        if char == '\n':
            line += 1

        if is_comment:
            if char == '\n':
                is_comment = False
        elif is_str:
            if char == '\"':
                tokens.append (token (TOKEN_VALUE_STR, name, line))
                name = ""
                is_str = False
            elif char == '\\':
                it += 1
                char = code [it]
                if char == '\\':
                    name += '\\'
                elif char == 'n':
                    name += '\n'
                elif char == 't':
                    name += '\t'
                elif char == 'r':
                    name += '\r'
                elif char == '\"':
                    name += '\"'
            else:
                name += char
        else:
            if char in " \n\t()[]{}\\\"#;":
                if name != "":
                    tokens.append (token (get_token_type (name), name, line))
                    name = ""

                if char == '(':
                    tokens.append (token (TOKEN_P_OPEN, "", line))
                elif char == ')':
                    tokens.append (token (TOKEN_P_CLOSED, "", line))
                elif char == '[':
                    tokens.append (token (TOKEN_L_OPEN, "", line))
                elif char == ']':
                    tokens.append (token (TOKEN_L_CLOSED, "", line))
                elif char == '{':
                    tokens.append (token (TOKEN_A_OPEN, "", line))
                elif char == '}':
                    tokens.append (token (TOKEN_A_CLOSED, "", line))
                elif char == '\"':
                    is_str = True
                elif char == '\\':
                    it += 1
                    char = code [it]

                    if char == '\\':
                        it += 1
                        char = code [it]
                        if char == '\\':
                            tokens.append (token (TOKEN_VALUE_CHAR, '\\', line))
                        elif char == 'n':
                            tokens.append (token (TOKEN_VALUE_CHAR, '\n', line))
                        elif char == 't':
                            tokens.append (token (TOKEN_VALUE_CHAR, '\t', line))
                        elif char == 'r':
                            tokens.append (token (TOKEN_VALUE_CHAR, '\r', line))
                        elif char == 's':
                            tokens.append (token (TOKEN_VALUE_CHAR, ' ', line))
                        else:
                            print ("Tokenizer Error: Expected '\\', 'n', 't', 's' or 'r' after \\\\")
                            sys.exit ()
                    else:
                        tokens.append (token (TOKEN_VALUE_CHAR, char, line))

                elif char == '#' or char == ';':
                    is_comment = True
            else:
                name += char
        it += 1

    if name != "":
        tokens.append (token (get_token_type (name), name, line))
        name = ""

    return tokens
