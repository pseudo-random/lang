# MIT License
#
# Copyright (c) 2018 pseudo-random <josh.leh.2018@gmail.com>
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

import utils
from consts import *
from parser import node

names = {}
name_count = 0

def escape (text):
    return text.replace ("\\", "\\\\").replace ("\n", "\\n").replace ("\t", "\\t").replace ("\"", "\\\"").replace ("\r", "\\r")

def generate_name_id (name):
    global names, name_count

    if not name in names:
        names[name] = name_count
        name_count += 1

    return names[name]

def generate_name (node):
    return "__" + str (generate_name_id (node.value))

def generate_symbol_tables ():
    code = ""
    code += "let symbolCount = " + str (name_count) + ";\n"
    code += "let symbolIDs = {};\n"
    code += "let symbolNames = {};\n"

    for name in names:
        ID = names[name]
        code += "symbolIDs[\"" + name + "\"] = " + str (ID) + ";\n"
        code += "symbolNames[" + str (ID) + "] = \"" + name + "\";\n"

    return code

def generate_list (node):
    if len (node) == 0:
        return "new ListEmpty ()"
    else:
        return "new List (" + generate (node[0]) + ", " + generate_list (node [1:]) + ")"

def generate_array (node):
    return "new _Map (" + ",".join ([",".join ([generate (x[0]), generate (x[1])]) for x in node]) + ")"

def generate_value (value_type, value):
    return "new " + value_type + " (" + value + ")"


def generate_internal (node):
    name = node[0].value

    operators = {
        "add": " + ", "sub": " - ",
        "mul": " * ", "div": " / ",
        "mod": " % ",

        "gt": ">",
        "lt": "<",

        "bit-and": "&",
        "bit-or": "|",
        "bit-xor": "^",
        "bit-lshift": "<<",
        "bit-rshift": ">>",
    }

    funcs = {
        "eq": "eq",
        "type": "type",
        "to-int": "toInt",
        "to-str": "toStr",
        "to-symbol": "toSymbol",
        "to-char": "toChar",
        "prn": "printToStr",

        "floor": "Math.floor",
        "round": "Math.round",
        "ceil": "Math.ceil",
        "sqrt": "Math.sqrt",

        "write": "write",
        "print": "writeln",
        "read": "read",
    }

    methods = {
        "first": "first",
        "rest": "rest",
        "prepend": "prepend",
        "nth": "nth",
        "index": "nth",
        "empty": "isEmpty",
        "len": "len",

        "insert": "insert",
        "remove": "remove",
        "keys": "keys",
        "empty-of": "emptyOf",
    }

    if name in operators:
        return operators[name].join ([generate(x) for x in node[1:]])
    elif name in funcs:
        return funcs[name] + "(" + ",".join ([generate (x) for x in node [1:]]) + ")"
    elif name in methods:
        return generate (node[1]) + "." + methods[name] + "(" + ",".join ([generate (x) for x in node [2:]]) + ")"
    elif name == "js":
        return node[1].value + "(" + ",".join ([generate (x) for x in node[2:]]) + ")"
    elif name == "js-require":
        return "const " + node[1].value + " = require (\"" + node[1].value + "\")"
    elif name == "js-method":
        return "(" + generate (node[1]) + ")." + node[2].value + "(" + ",".join ([generate (x) for x in node [3:]]) + ")"
    else:
        raise Exception ("Unknown internal: " + name)

def generate_typedef (node):
    params = ",".join ([
        generate_name (name)
        for name in node[1:]
    ])

    typename = "this.type = \"" + node[0].value + "\";\n"

    fields = ";\n".join ([
        "this." + generate_name (name) + " = " + generate_name (name)
        for name in node[1:]
    ])

    nth_cases = ";\n".join ([
        "if (x._id == " + str (names[name.value]) + ") { return this." + generate_name (name) + "}"
        for name in node[1:]
    ] + ["return null"])

    nth = "this.nth = function (x) {" + nth_cases + "}"

    eq_cases = " && ".join ([
        "eq(this." + generate_name (name) + ", x." + generate_name (name) + ")"
        for name in node[1:]
    ] + ["type (this).eq (type (x))"])
    eq = "this.eq = function (x) { return (" + eq_cases + ") }"

    to_string = "this.toString = function () { return \"" + node[0].value + "\" }"

    body = typename + ";\n" + fields + ";\n" + nth + ";\n" + eq + ";\n" + to_string

    return "(function (" + params + ") { return new function (" + params + ") {" + body + "} (" + params + ") })"

def generate (node):
    if node.type == NODE_S_EXPR:
        return generate (node [0]) + "(" + ",".join ([generate (x) for x in node[1:]]) + ")"

    elif node.type == NODE_IF:
        return "(istrue (" + generate (node [0]) + ") ? " + generate (node [1]) + " : " + generate (node [2]) + ")"
    elif node.type == NODE_FN:
        params = ",".join ([generate (x) for x in node [0].children])
        body = ";\n".join ([generate (x) for x in node [1:]])
        return "((" + params + ") => {;\n" + body + ";\n})"
    elif node.type == NODE_DO:
        return "(() => {;\n" + ";\n".join ([generate (x) for x in node [0:-1]]) + ";\n" + "return " + generate (node[-1]) + ";\n})()"
    elif node.type == NODE_DEF:
        return "let " + generate_name (node[0]) + " /* " + node[0].value + " */ " + " = " + generate (node [1])
    elif node.type == NODE_INTERNAL:
        return generate_internal (node)
    elif node.type == NODE_IF_STATEMENT:
        return "if (istrue (" + generate (node[0]) + ")) {;\n" + generate (node[1]) + ";\n} else {;\n" + generate (node[2]) + ";\n}"
    elif node.type == NODE_BLOCK:
        return "{;\n" + ";\n".join ([generate (x) for x in node]) + ";\n}"
    elif node.type == NODE_WHILE:
        return "while (" + generate (node[0]) + ") {;\n" + ";\n".join ([generate (x) for x in node[1:]]) + ";\n}"
    elif node.type == NODE_RECUR:
        return "continue"
    elif node.type == NODE_UPDATE_VALUES:
        return generate (node[0]) + " = " + generate (node[1])
    elif node.type == NODE_ROOT:
        with open ("src/compiler/runtime/runtime.js") as f:
            runtime = f.read ()
        source = ";\n".join ([generate (x) for x in node])
        return "{\n" + runtime + ";\n" + generate_symbol_tables () + ";\n" + source + ";\n}"
    elif node.type == NODE_RETURN:
        return "return " + generate (node[0])
    elif node.type == NODE_SPREAD:
        return "..." + generate (node[0])
    elif node.type == NODE_TYPE:
        return generate_typedef (node)

    elif node.type == NODE_NAME:
        return generate_name (node)
    elif node.type == NODE_LITERAL_INT:
        return str (node.value)
    elif node.type == NODE_LITERAL_FLOAT:
        return str (node.value)
    elif node.type == NODE_LITERAL_BOOL:
        return str (node.value)
    elif node.type == NODE_NIL:
        return "null"
    elif node.type == NODE_LIST:
        return generate_list (node)
    elif node.type == NODE_ARRAY:
        return generate_array (node)
    elif node.type == NODE_SYMBOL:
        return generate_value ("Symbol", str (generate_name_id (node.value)))
    elif node.type == NODE_LITERAL_CHAR:
        return generate_value ("Char", "\"" + escape (node.value) + "\"")
    elif node.type == NODE_LIST_MUTABLE:
        return "[" + ",".join ([generate (x) for x in node]) + "]"
    elif node.type == NODE_STRING:
        return "\"" + escape (node.value) + "\""
    else:
        return ""
