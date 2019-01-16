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


# Tokens
TOKEN_COLON = 1

TOKEN_P_OPEN = 2
TOKEN_P_CLOSED = 3
TOKEN_L_OPEN = 4
TOKEN_L_CLOSED = 5
TOKEN_A_OPEN = 6
TOKEN_A_CLOSED = 7

TOKEN_NAME = 8
TOKEN_VALUE_INT = 9
TOKEN_VALUE_FLOAT = 10
TOKEN_VALUE_BOOL = 11
TOKEN_VALUE_STR = 12
TOKEN_VALUE_CHAR = 13

token_names = [
    "newline",
    "colon",

    "p_closed",
    "p_open",
    "l_open",
    "l_closed",
    "a_open",
    "a_closed",

    "name",
    "value_int",
    "value_float",
    "value_bool",
    "value_str",
    "value_char"
]

# Nodes
NODE_ROOT = 0

NODE_S_EXPR = 1
NODE_LIST = 2
NODE_NAME = 3

NODE_SYMBOL = 4
NODE_ARRAY = 5
NODE_ARRAY_ITEM = 6

NODE_LITERAL_BOOL = 7
NODE_LITERAL_INT = 8
NODE_LITERAL_FLOAT = 9
NODE_LITERAL_STR = 10
NODE_LITERAL_CHAR = 11
NODE_NIL = 12

NODE_RETURN = 13
NODE_FN = 14
NODE_IF = 15
NODE_DO = 16
NODE_INTERNAL = 17
NODE_DEF = 18
NODE_RECUR = 19
NODE_WHILE = 20
NODE_IF_STATEMENT = 21
NODE_BLOCK = 22
NODE_UPDATE_VALUES = 23 # rename to NODE_ASSIGN?
NODE_LIST_MUTABLE = 24
NODE_SPREAD = 25
NODE_STRING = 26
NODE_TYPE = 27

NODE_EXPAND = -1

node_names = [
    "root",

    "s_expr",
    "list",
    "name",
    "symbol",
    "array",
    "item",

    "literal_bool",
    "literal_int",
    "literal_float",
    "literal_str",
    "literal_char",
    "nil",

    "return",
    "fn",
    "if",
    "do",
    "internal",
    "def",
    "recur",
    "while",
    "if_statement",
    "block",
    "update_values",
    "list_mutable",
    "spread",
    "string",

    "expand"
]

# Types

TYPE_INT = 0
TYPE_FLOAT = 1
TYPE_BOOL = 2
TYPE_SYMBOL = 3
TYPE_CHAR = 4

TYPE_ARRAY = 5
TYPE_FUNC = 6
TYPE_LIST = 7
TYPE_TYPE = 8
