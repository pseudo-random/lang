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

def read_file (path):
    my_file = open (path, "r")
    contents = my_file.read ()
    my_file.close ()
    return contents

def is_bool (s):
    return s == "true" or s == "false"

def is_int (s):
    return s.strip ("+-").isdigit ()

def is_hex (s):
    return s.startswith ("0x")

def is_float (s):
    return s.strip ("+-").replace (".", "").isdigit () and s.count (".") <= 1

class CompilerError (Exception):
    def __init__(self, text, line=0):
        self.text = text
        self.line = line

    def __str__ (self):
        return "Compiler Error in line " + str (self.line) + ": " + self.text
