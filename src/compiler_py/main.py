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

import sys
from consts import *

import utils
import tokenizer
import parser
import passes
import macros
import generator

def main ():
    if len (sys.argv) != 2:
        print ("./compiler.py <input>")
        sys.exit ()

    path = sys.argv[1]
    code = utils.read_file ("lib/std/std.txt") + utils.read_file (path)

    tokens = tokenizer.tokenize (code)

    ast = parser.parse (tokens)

    try:
        env = {"file_path": path, "imports": []}
        ast = passes.remove_quotes (ast)
        ast = passes.expand_use (ast, env)
        ast = macros.expand_macros (ast, env)
        ast = passes.remove_expand_nodes (ast)
        passes.transform_special_forms (ast)
        passes.convert_to_statements (ast)
        passes.add_return_statements (ast)
        passes.find_tail_recursive_functions (ast)
        passes.optimize_tail_recursive_functions (ast)
        passes.convert_varargs_to_spread (ast)

        print (generator.generate (ast))
    except utils.CompilerError as e:
        print (e)

if __name__ == "__main__":
    main()
