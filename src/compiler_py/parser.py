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

import utils, sys
import tokenizer
from consts import *

class node:
    def __init__ (self, node_type, children=None, value="", line=None):
        self.type = node_type
        self.value = value
        self.line = line

        if children == None:
            self.children = []
        else:
            self.children = children

    def push (self, child):
        self.children.append (child)

    def log (self, indent=0, names=None):
        if names == None:
            names = node_names

        print ("  "*indent+names[self.type] + ":", self.value)
        for child in self.children:
            child.log (indent+1, names)

    def __getitem__ (self, x):
        return self.children[x]

    def __len__ (self):
        return len (self.children)

    def __bool__ (self):
        return True

    def __setitem__ (self, key, value):
        self.children[key] = value

def parse (tokens):
    cur = -1

    def next (t):
        nonlocal cur
        if cur + 1 < len (tokens):
            if tokens[cur+1].type == t:
                cur += 1
                return True
        return False

    def find (t, accept):
        nonlocal cur
        x = cur+1
        while True:
            if tokens[x].type == t:
                return True
            elif tokens[x].type in accept:
                pass
            else:
                return False

            x += 1

    def param ():
        nonlocal cur
        if next (TOKEN_NAME):
            if tokens[cur].value == "nil":
                return node (NODE_NIL, line=tokens[cur].line)
            elif tokens[cur].value[0] == ":":
                return node (NODE_S_EXPR, [
                    node (NODE_NAME, [], "quote"),
                    node (NODE_NAME, [], tokens[cur].value[1:], line=tokens[cur].line)
                ])
            elif "/" in tokens[cur].value and tokens[cur].value[0] != "/":
                path = tokens[cur].value.split ("/")
                node_nth = node (NODE_NAME, [], path[0], line=tokens[cur].line)
                for x in path[1:]:
                    node_nth = node (NODE_S_EXPR, [
                        node (NODE_NAME, [], "nth"),
                        node_nth,
                        node (NODE_SYMBOL, [], x)
                    ])
                return node_nth
            return node (NODE_NAME, [], tokens[cur].value, line=tokens[cur].line)
        elif next (TOKEN_VALUE_BOOL):
            return node (NODE_LITERAL_BOOL, [], tokens[cur].value, line=tokens[cur].line)
        elif next (TOKEN_VALUE_INT):
            if tokens[cur].value.startswith ("0x"):
                return node (NODE_LITERAL_INT, [], str (int (tokens[cur].value[2:], 16)), line=tokens[cur].line)
            return node (NODE_LITERAL_INT, [], tokens[cur].value, line=tokens[cur].line)
        elif next (TOKEN_VALUE_FLOAT):
            return node (NODE_LITERAL_FLOAT, [], tokens[cur].value, line=tokens[cur].line)
        elif next (TOKEN_VALUE_CHAR):
            return node (NODE_LITERAL_CHAR, [], tokens[cur].value, line=tokens[cur].line)
        elif next (TOKEN_VALUE_STR):
            return node (NODE_STRING, [], tokens[cur].value, line=tokens[cur].line)

        elif next (TOKEN_P_OPEN):
            cur -= 1
            return s_expr ()
        elif next (TOKEN_L_OPEN):
            cur -= 1
            node_list = s_expr (TOKEN_L_OPEN, TOKEN_L_CLOSED)

            for it, child in enumerate (node_list.children):
                node_list.children[it] = node (NODE_S_EXPR, [
                    node (NODE_NAME, [], "unquote"),
                    child
                ])

            return node (NODE_S_EXPR, [
                node (NODE_NAME, [], "quote"),
                node_list
            ])

        elif next (TOKEN_A_OPEN):
            cur -= 1
            return array ()

        return None

    def s_expr (begin=TOKEN_P_OPEN, end=TOKEN_P_CLOSED):
        if not next (begin):
            return None

        node_s_expr = node (NODE_S_EXPR, line=tokens[cur].line)
        while True:
            node_param = param ()
            if node_param:
                node_s_expr.push (node_param)
            else:
                break

        if not next (end):
            return None

        return node_s_expr

    def array (begin=TOKEN_A_OPEN, end=TOKEN_A_CLOSED):
        if not next (begin):
            return None

        node_array = node (NODE_ARRAY, line=tokens[cur].line)
        it = 0
        while True:
            node_item = node (NODE_ARRAY_ITEM)

            node_param = param ()
            if node_param:
                node_item.push (node_param)
            else:
                break

            node_item.push (param ())


            node_array.push (node_item)
            it += 1

        if not next (end):
            return None

        #if len(node_array.children) == 0:
        #    return None

        return node_array

    node_root = node (NODE_ROOT)
    node_param = param ()
    while node_param:
        node_root.push (node_param)
        node_param = param ()

    return node_root
