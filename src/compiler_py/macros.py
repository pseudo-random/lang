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

# Built-In Macros

import os.path
from parser import node
from consts import *
from utils import CompilerError
import utils, tokenizer, parser, passes

sym_count = 0
def gen_sym ():
    global sym_count
    sym_count += 1
    return "~" + str (sym_count)

def macro_defn (ast, env):
    node_def = node (NODE_S_EXPR)
    node_def.push (node (NODE_NAME, [], "def"))

    node_def.push (ast[1])

    node_fn = node (NODE_S_EXPR)
    node_fn.push (node (NODE_NAME, [], "fn"))

    for child in ast.children [2:]:
        node_fn.push (child)

    node_def.push (node_fn)

    return node_def

def macro_when (ast, env):
    node_if = node (NODE_S_EXPR, [
        node (NODE_NAME, [], "if")
    ])

    node_if.push (ast[1])

    node_do = node (NODE_S_EXPR, [
        node (NODE_NAME, [], "do")
    ])

    for child in ast.children[2:]:
        node_do.push (child)

    node_if.push (node_do)
    node_if.push (node (NODE_LITERAL_BOOL, [], "false"))

    return node_if

def macro_unless (ast, env):
    node_if = node (NODE_S_EXPR, [
        node (NODE_NAME, [], "if")
    ])

    node_if.push (ast[1])
    node_if.push (node (NODE_LITERAL_BOOL, [], "false"))

    node_do = node (NODE_S_EXPR, [
        node (NODE_NAME, [], "do")
    ])

    for child in ast.children[2:]:
        node_do.push (child)

    node_if.push (node_do)

    return node_if

# (dotimes [it 10] (print it))
# ((fn [it to]
#   (unless (= it to)
#     (print it)
#     (recur (+ 1 it) to))) 0 10)

def macro_dotimes (ast, env):
    pass

def macro_pipe (ast, env):
    for it in range (2, len (ast)):
        ast.children[it].children.insert (1, ast.children[it-1])

    return ast.children[-1]

# (curry + 1)
# (fn [x] (+ x 1))

def macro_curry (ast, env):
    x = gen_sym ()

    node_fn = node (NODE_S_EXPR, [
        node (NODE_NAME, [], "fn"),
        node (NODE_LIST, [
            node (NODE_NAME, [], x)
        ]),
        node (NODE_S_EXPR, [
            ast[1],
            node (NODE_NAME, [], x),
            *ast[2:]
        ])
    ])

    return node_fn

# (return-if (func x) ...)
# (do (def x (func x)) (if x x (do ...)))

def macro_return_if (ast, env):
    x = gen_sym ()

    node_def = node (NODE_S_EXPR, [
        node (NODE_NAME, [], "def"),
        node (NODE_NAME, [], x),
        ast[1]
    ])

    node_if = node (NODE_S_EXPR, [
        node (NODE_NAME, [], "if"),
        node (NODE_NAME, [], x),
        node (NODE_NAME, [], x),

        node (NODE_S_EXPR, [
            node (NODE_NAME, [], "do"),
            *ast[2:]
        ]),
    ])

    node_do = node (NODE_S_EXPR, [
        node (NODE_NAME, [], "do"),
        node_def,
        node_if
    ])

    return node_do


# (or a b c)
# (return-if a (or b c))
# (return-if a (return-if b c))

def macro_or (ast, env):
    if len (ast) == 2:
        return ast[1]
    else:
        return node (NODE_S_EXPR, [
            node (NODE_NAME, [], "return-if"),
            ast[1],
            node (NODE_S_EXPR, [
                node (NODE_NAME, [], "or"),
                *ast[2:]
            ])
        ])

# (and a b c)
# (if a (and b c) false)

def macro_and (ast, env):
    if len (ast) == 2:
        return ast[1]
    else:
        return node (NODE_S_EXPR, [
            node (NODE_NAME, [], "when"),
            ast[1],
            node (NODE_S_EXPR, [
                node (NODE_NAME, [], "and"),
                *ast[2:]
            ])
        ])

# (deftype str list? (: all? char?))
# (defn str? [x]
#   (and (list? x) ((: all? char?) x)))

def macro_defpattern (ast, env):
    return node (NODE_S_EXPR, [
        node (NODE_NAME, [], "def"),
        ast[1],
        node (NODE_S_EXPR, [
            node (NODE_NAME, [], "pattern"),
            *ast[2:]
        ])
    ])

# (cond
#   (= x 1) (print 1)
#   (= x 2) (print 2)
#   :else   (print "?"))

# (if (= x 1)
#   (print 1)
#   (if (= x 2)
#     (print 2)
#     (print "?")))

def macro_cond (ast, env):
    if len (ast) <= 5:
        return node (NODE_S_EXPR, [
            node (NODE_NAME, [], "if"),
            ast[1], ast[2],
            ast[4]
        ])
    else:
        return node (NODE_S_EXPR, [
            node (NODE_NAME, [], "if"),
            ast[1], ast[2],
            node (NODE_S_EXPR, [
                node (NODE_NAME, [], "cond"),
                *ast[3:]
            ])
        ])

# (module (def a 10))
# ((fn [] (def a 10) {:a a}))

def macro_module (ast, env):
    ast.children = [expand_macros (x, env) for x in ast.children]

    defs = node (NODE_ARRAY, [
        node (NODE_ARRAY_ITEM, [
            node (NODE_SYMBOL, [], x[1].value),
            node (NODE_NAME, [], x[1].value)
        ])
        for x in ast[1:]
        if x.type == NODE_S_EXPR and len (x) == 3 and x [0].value == "def*"
    ])

    return node (NODE_S_EXPR, [
        node (NODE_S_EXPR, [
            node (NODE_NAME, [], "fn"),
            node (NODE_LIST, []),
            *ast[1:],
            defs
        ])
    ])

def macro_defmodule (ast, env):
    node_def = node (NODE_S_EXPR)
    node_def.push (node (NODE_NAME, [], "def"))

    node_def.push (ast[1])

    node_fn = node (NODE_S_EXPR)
    node_fn.push (node (NODE_NAME, [], "module"))

    for child in ast.children [2:]:
        node_fn.push (child)

    node_def.push (node_fn)

    return node_def

def macro_import (ast, env):
    path = env["file_path"].split ("/")
    path [-1] = ast[1].value + ".txt"
    file_path = "/".join (path)

    if not os.path.isfile (file_path):
        file_path = "lib/" + ast[1].value + "/" + ast[1].value + ".txt"

    code = utils.read_file (file_path)
    tokens = tokenizer.tokenize (code)
    tree = parser.parse (tokens)
    tree = node (NODE_S_EXPR, [
        node (NODE_NAME, [], "defmodule"),
        ast[1],
        *tree.children
    ])

    module_env = {"imports": [], "file_path": file_path}

    tree = passes.remove_quotes (tree)
    tree = passes.expand_use (tree, module_env)
    tree = expand_macros (tree, module_env)

    return tree

def macro_use_quoted (ast, env):
    path = env["file_path"].split ("/")
    path [-1] = ast[1].value + ".txt"

    code = utils.read_file ("/".join (path))
    tokens = tokenizer.tokenize (code)
    tree = parser.parse (tokens)
    tree.children = [
        node (NODE_S_EXPR, [
            node (NODE_NAME, [], "quote"),
            node (NODE_S_EXPR, tree.children)
        ])
    ]

    tree = passes.remove_quotes (tree)
    tree.type = NODE_EXPAND

    return tree

def macro_fn (ast, env):
    ast[0].value = "fn*"
    return ast


def macro_def (ast, env):
    if len (ast) > 3:
        raise CompilerError ("Macro def expects 2 arguments, " + str (len (ast)-1) + " given. Did you mean defn?", line=ast.line)
    elif len (ast) < 3:
        raise CompilerError ("Macro def expects 2 arguments, " + str (len (ast)-1) + " given: (def name value)", line=ast.line)

    ast[0].value = "def*"
    return ast

def macro_defmacro (ast, env):
    return node (NODE_NIL, [])

def macro_deftype (ast, env):
    return node (NODE_S_EXPR, [
        node (NODE_NAME, [], "def*"),
        node (NODE_NAME, [], ast[1].value + "*"),
        node (NODE_S_EXPR, [
            node (NODE_NAME, [], "type"),
            *ast[1:]
        ])
    ])

def macro_let (ast, env):
    if len (ast) < 3:
        raise CompilerError ("Macro let expects 2 or more arguments (let bindings & body).", line=ast.line)

    return node (NODE_S_EXPR, [
        node (NODE_NAME, [], "do"),
        *[
            node (NODE_S_EXPR, [
                node (NODE_NAME, [], "def"),
                ast[1][it],
                ast[1][it+1]
            ])
            for it in range (0, len (ast[1]), 2)
        ],
        *ast[2:]
    ])

# (match x
#   abc)
def macro_match (ast, env):
    if len (ast) == 2:
        return node (NODE_NIL, [], "nil")
    if len (ast) == 3:
        return ast[-1]

    return node (NODE_S_EXPR, [
        node (NODE_NAME, [], "if"),
        node (NODE_S_EXPR, [
            node (NODE_NAME, [], "="),
            ast[1],
            ast[2]
        ]),
        ast[3],
        node (NODE_S_EXPR, [
            node (NODE_NAME, [], "match"),
            ast[1],
            *ast[3:]
        ])
    ])

def expand_macros (ast, env):
    macros = {
        "def" : macro_def,
        "fn" : macro_fn,

        "defn" : macro_defn,
        "when": macro_when,
        "unless": macro_unless,
        "->": macro_pipe,
        #"dotimes": macro_dotimes,
        "curry": macro_curry,
        "return-if": macro_return_if,
        "or": macro_or,
        "and": macro_and,
        "defpattern": macro_defpattern,
        "cond" : macro_cond,
        "module" : macro_module,
        "defmodule" : macro_defmodule,
        "use-quoted": macro_use_quoted,
        "defmacro": macro_defmacro,
        "deftype" : macro_deftype,
        "let": macro_let,
        "import": macro_import,
        "match": macro_match
    }

    def walk (ast_node):
        if ast_node.type == NODE_S_EXPR and len (ast_node) > 0:
            name = ast_node[0].value
            if name in macros:
                return walk (macros[name](ast_node, env))

        for it, child in enumerate (ast_node.children):
            ast_node.children[it] = walk (child)

        return ast_node

    return walk (ast)
