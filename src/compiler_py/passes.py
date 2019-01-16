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

from consts import *
from parser import node
import os

def remove_quotes (my_node, depth=0):
    if my_node.type == NODE_S_EXPR:
        if len (my_node) > 0 and my_node[0].value == "quote":
            if depth > 0:
                node_array = node (NODE_LIST if depth > 0 else NODE_S_EXPR, [], line=my_node.line)
                for it, child in enumerate (my_node.children):
                    node_array.push (remove_quotes (child, depth+1))
                return node_array
            else:
                return remove_quotes (my_node[1], depth+1)
        elif len (my_node) > 0 and my_node[0].value == "unquote":
            if depth > 1:
                node_array = node (NODE_LIST if depth > 0 else NODE_S_EXPR, [], line=my_node.line)
                for it, child in enumerate (my_node.children):
                    node_array.push (remove_quotes (child, depth-1))
                return node_array
            else:
                #print ("Unquote")
                #my_node.log ()
                return remove_quotes (my_node[1], depth-1)
        else:
            node_array = node (NODE_LIST if depth > 0 else NODE_S_EXPR, [], line=my_node.line)
            for child in my_node.children:
                node_array.push (remove_quotes (child, depth))
            return node_array
    elif my_node.type == NODE_NAME:
        return node (NODE_SYMBOL if depth > 0 else NODE_NAME, [], my_node.value, line=my_node.line)
    elif my_node.type == NODE_ARRAY_ITEM:
        return node (NODE_ARRAY_ITEM, [
            remove_quotes (my_node[0], 0),
            remove_quotes (my_node[1], depth)
        ])
    else:
        n = node (my_node.type, [], my_node.value, line=my_node.line)
        for child in my_node.children:
            n.push (remove_quotes (child, depth))
        return n

def expand_use (ast, env):
    imports = []

    def walk (ast_node):
        if ast_node.type == NODE_S_EXPR and len (ast_node) > 0:
            name = ast_node[0].value
            if name == "use":
                node_expand = node (NODE_EXPAND, [])
                for lib in ast_node[1:]:
                    if lib.value in env["imports"]:
                        continue

                    env["imports"].append (lib.value)

                    file_name = lib.value + ".txt"

                    path = env["file_path"].split ("/")
                    path [-1] = file_name
                    file_path = "/".join (path)

                    if not os.path.isfile (file_path):
                        file_path = "lib/" + lib.value + "/" + file_name

                    import utils, tokenizer, parser, passes
                    code = utils.read_file (file_path)
                    tokens = tokenizer.tokenize (code)
                    tree = parser.parse (tokens)
                    tree = passes.remove_quotes (tree)
                    tree = expand_use (tree, {
                        "file_path": file_path,
                        "imports": env["imports"]
                    })
                    tree.type = NODE_EXPAND
                    node_expand.push (tree)

                return node_expand

        for it, child in enumerate (ast_node.children):
            ast_node.children[it] = walk (child)

        return ast_node

    return walk (ast)

def remove_expand_nodes (ast):
    def walk (ast_node):
        children = []
        found = False
        for child in ast_node.children:
            if child.type == NODE_EXPAND:
                children += child.children
                found = True
            else:
                children.append (child)

        if found:
            ast_node.children = children
            ast_node = walk (ast_node)
            return ast_node
        else:
            for it, child in enumerate (children):
                children[it] = walk (child)

            ast_node.children = children
            return ast_node


    return walk (ast)

def transform_special_forms (ast):
    special_forms = {
        "fn*"  : NODE_FN,
        "do"   : NODE_DO,
        "if"   : NODE_IF,
        "def*" : NODE_DEF,
        "recur": NODE_RECUR,
        "type" : NODE_TYPE,

        "internal": NODE_INTERNAL,
    }

    if ast.type == NODE_S_EXPR and ast[0].value in special_forms:
        ast.type = special_forms [ast[0].value]
        ast.children = ast.children[1:]

    for child in ast:
        transform_special_forms (child)

def add_return_statements (ast):
    def add_return_statement (ast_node):
        if ast_node.type == NODE_IF_STATEMENT:
            ast_node.children[1] = add_return_statement (ast_node[1])
            ast_node.children[2] = add_return_statement (ast_node[2])
            return ast_node
        elif ast_node.type == NODE_BLOCK:
            ast_node.children[-1] = add_return_statement (ast_node[-1])
            return ast_node
        elif ast_node.type == NODE_RECUR:
            return ast_node
        else:
            return node (NODE_RETURN, [ast_node])

    if ast.type == NODE_FN:
        ast.children[-1] = add_return_statement (ast.children[-1])

    for child in ast:
        add_return_statements (child)

def convert_to_statements (ast, statement_level=True):
    if statement_level:
        if ast.type == NODE_IF:
            ast.type = NODE_IF_STATEMENT
        elif ast.type == NODE_DO:
            ast.type = NODE_BLOCK

    for it, child in enumerate (ast):
        if ast.type in [NODE_FN, NODE_IF_STATEMENT] and it != 0:
            convert_to_statements (child, statement_level=True)
        elif ast.type == NODE_BLOCK:
            convert_to_statements (child, statement_level=True)
        else:
            convert_to_statements (child, statement_level=False)

def find_tail_recursive_functions (ast):
    def is_tail_recursive (fn_node):
        if fn_node.type == NODE_RECUR:
            return True
        elif fn_node.type == NODE_IF_STATEMENT:
            for child in fn_node [1:]:
                  if is_tail_recursive (child):
                        return True
        elif fn_node.type == NODE_BLOCK:
            for child in fn_node:
                if is_tail_recursive (child):
                    return True
        return False

    if ast.type == NODE_FN:
        ast.tail_recursive = False
        for child in ast [1:]:
            if is_tail_recursive (child):
                ast.tail_recursive = True
                break

    for child in ast:
        find_tail_recursive_functions (child)

def optimize_tail_recursive_functions (ast):
    def expand_recur (fn_node, fn):
        if fn_node.type == NODE_RECUR:
            return node (NODE_BLOCK, [
                node (NODE_UPDATE_VALUES, [
                    node (NODE_LIST_MUTABLE, fn[0].children),
                    node (NODE_LIST_MUTABLE, fn_node.children)
                ]),
                fn_node
            ])
        elif fn_node.type == NODE_IF_STATEMENT:
            fn_node.children[1] = expand_recur (fn_node[1], fn)
            fn_node.children[2] = expand_recur (fn_node[2], fn)
        elif fn_node.type == NODE_BLOCK:
            for it, child in enumerate (fn_node):
                fn_node.children[it] = expand_recur (child, fn)

        return fn_node

    if ast.type == NODE_FN and ast.tail_recursive:
        for it, child in enumerate (ast [1:]):
            ast.children[it+1] = expand_recur (child, ast)

        ast.children = [
            ast.children[0],
            node (NODE_WHILE, [
                node (NODE_LITERAL_BOOL, [], "true"),
                *ast.children[1:]
            ])
        ]

    for child in ast:
        optimize_tail_recursive_functions (child)


def convert_varargs_to_spread (ast):
    if ast.type == NODE_FN:
        if ast[0].type == NODE_NAME:
            ast[0] = node (NODE_LIST, [
                node (NODE_SPREAD, [
                    ast[0]
                ])
            ])

    for child in ast:
        convert_varargs_to_spread (child)
