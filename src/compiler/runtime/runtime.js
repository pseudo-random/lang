let istrue = (x) => x !== null && x !== false

function eq (x, y) {
  if (typeof x === "object" && typeof y === "object") {
    if ((x === null) != (y === null)) {
      return false
    } else if (x === null && y === null) {
      return true
    } else {
      return (x.eq (y))
    }
  } else if (typeof x === "object" && typeof y === "string") {
    return x.eq (y)
  } else if (typeof x === "string" && typeof y === "object") {
    return y.eq (x)
  } else {
    return x === y
  }
  return false
}

function type (x) {
  if (x === null) {
    return new Type ("nil")
  } else if (typeof x === "object") {
    return new Type (x.type)
  } else if (typeof x === "number") {
    if (x % 1 === 0) {
      return new Type ("int")
    } else {
      return new Type ("float")
    }
  } else {
    return new Type (typeof x)
  }
  return new Type ("nil")
}

function toInt (x) {
  if (x === null) {
    return 0
  } else if (typeof x === "object") {
    return x.toInt ()
  } else if (typeof x === "number") {
    return x | 0
  } else {
    return (istrue (x) ? 1 : 0)
  }
}

function toStr (x) {
  if (x === null) {
    return "nil"
  } else if (typeof x === "object" || typeof x === "number") {
    return x.toString ()
  } else if (typeof x === "boolean") {
    return (x ? "true" : "false")
  } else if (typeof x === "string") {
    return x
  } else {
    return ""
  }
}

function toChar (x) {
  if (typeof x === "number") {
    return new Char (String.fromCodePoint (x | 0))
  }
  return null
}

function printToStr (x) {
  if (x === null) {
    return "nil"
  } else if (typeof x === "object") {
    return x.printToString ()
  } else if (typeof x === "number") {
    return x.toString ()
  } else if (typeof x === "boolean") {
    return (x ? "true" : "false")
  } else if (typeof x === "string") {
    return x.printToStr ()
  } else {
    return ""
  }
}

function toSymbol (x) {
  if (typeof x === "string") {
    if (!symbols.IDs.hasOwnProperty (x)) {
      let id = ++symbols.count
      symbols.IDs[x] = id
      symbols.names[id] = x
    }
    return new Symbol (symbols.IDs[x])
  } else if  (typeof x === "number") {
    return new Symbol (x)
  }
  return null
}

function apply (func, args) {
  return func (...(args.toVector ()))
}

function toJS (x) {
  if (x === null) { return null }
  if (x.toJS) { return x.toJS () }
  return x
}

// I/O
let buffer = ""

function writeln (x) {
  write (x)
  write ("\n")
  return null
}

function write (x) {
  if (x === null)
    buffer += "nil"; // TODO: Define null.toString () => custom nil object?
  else
    buffer += x.toString ()

  if (buffer.includes ("\n")) {
    let lines = buffer.split ("\n")
    for (let it = 0; it < lines.length - 1; it++) {
      console.log (lines[it])
    }
    buffer = lines[lines.length - 1]
  }

  return null
}

function _hash (x) {
  if (typeof x === "object") {
    if (x === null) { return 0 }
    return x.hash ()
  } else {
    return x
  }
  return null
}

// Types
class Symbol {
  constructor (id) {
    this.type = "Symbol"
    this._id = id
  }

  hash () {
    return this._id
  }

  toInt () {
    return this._id
  }

  eq (other) {
    return this._id === other._id
  }

  toString () {
    return symbols.names [this._id]
  }

  printToString () {
    return symbols.names [this._id]
  }

  toJS () {
    return this.toString ()
  }
}

class Char {
  constructor (chr) {
    this.type = "Char"
    this._chr = chr
  }

  eq (other) {
    return this._chr === other._chr
  }

  toString () {
    return this._chr
  }

  toInt () {
    return this._chr.codePointAt (0)
  }

  hash () {
    return this._chr.codePointAt (0)
  }

  printToString () {
    if (this._chr === "\n")
      return "\\\\n"
    else if (this._chr === "\r")
      return "\\\\r"
    else if (this._chr === " ")
      return "\\\\s"
    else if (this._chr === "\\")
      return "\\\\\\"
    else if (this._chr === "\t")
      return "\\\\t"
    return "\\" + this._chr
  }

  toJS () {
    return this._chr
  }
}

class Type {
  constructor (name) {
    this.type = "Type"
    this._name = name
  }

  eq (other) {
    return this._name === other._name
  }

  toString () {
    return this._name
  }

  hash () {
    return this.type.hash () // TODO: Better hash algorithm
  }
}

class ListEmpty {
  constructor () {
    this.type = "List"
    this.isSeq = true
  }

  isEmpty () {
    return true
  }

  prepend (item) {
    return new List (item, this)
  }

  nth (index) {
    return null
  }

  first () {
    throw new RangeError ("Call first on empty list")
  }

  rest () {
    throw new RangeError ("Call rest on empty list")
  }

  toString () {
    return "()"
  }

  printToString () {
    return "()"
  }

  eq (other) {
    return other.type === "List" && other.isEmpty ()
  }

  hash () {
    return this.toString ()
  }

  emptyOf () {
    return new ListEmpty ()
  }

  len () {
    return 0
  }

  toVector () {
    return []
  }

  insert (key, value) {
    return new List(null, this).insert (key-1, value)
  }

  toJS () { return this.toVector () }
}

class List {
  constructor (first, rest) {
    this.type = "List"
    this.isSeq = true

    this._first = first
    this._rest = rest
  }


  first () {
    return this._first
  }

  rest () {
    return this._rest
  }

  prepend (item) {
    return new List (item, this)
  }

  isEmpty () {
    return false
  }

  nth (index) {
    let cur = this
    while (index > 0) {
      cur = cur.rest ()
      index--
    }
    return cur.first ()
  }

  len () {
    let length = 0, cur = this
    while (!cur.isEmpty ()) {
      cur = cur._rest
      length += 1
    }
    return length
  }

  toString () {
    let items = [], cur = this
    while (!cur.isEmpty ()) {
      items.push (toStr (cur._first))
      cur = cur._rest
    }
    return "(" + items.join (" ") + ")"
  }

  printToString () {
    let items = [], cur = this
    while (!cur.isEmpty ()) {
      items.push (printToStr (cur._first))
      cur = cur._rest
    }
    return "(" + items.join (" ") + ")"
  }

  eq (other) {
    if (other.type !== "List")
      return false

    let cur0 = this, cur1 = other
    while (!cur0.isEmpty() && !cur1.isEmpty()) {
      if (!eq(cur0._first, cur1.first ())) { return false }
      cur0 = cur0._rest
      cur1 = cur1.rest ()
    }
    return cur0.isEmpty () && cur1.isEmpty ()
  }

  hash () {
    return this.toString () // TODO
  }

  emptyOf () {
    return new ListEmpty ()
  }

  insert (key, value) {
    // TODO: Optimize, use loops instead of recursion?
    if (key === 0) {
      return new List (value, this._rest)
    }
    return new List (this._first, this._rest.insert (key-1, value))
  }

  toVector () {
    let vector = []
    let cur = this

    while (!cur.isEmpty ()) {
      vector.push (cur._first)
      cur = cur._rest
    }

    return vector
  }

  toJS () { return this.toVector () }
}

class _Map {
  constructor (...args) {
    this.type = "Map"
    this.isSeq = false // TODO: Implement seq

    this._keys = new Set ()
    this._map = {}

    for (let i = 0; i < args.length; i += 2) {
      let key = args[i],
      value = args[i+1]
      this._map[_hash (key)] = value
      this._keys.add (key)
    }
  }

  len () {
    return this._keys.size
  }

  nth (key) {
    if (!this._map.hasOwnProperty(_hash (key))) {
      return null
    }
    return this._map [_hash (key)]
  }

  insert (key, value) {
    let _map = Object.assign ({}, this._map)
    _map [_hash (key)] = value

    let _keys = new Set (this._keys)
    if (!this._map.hasOwnProperty (_hash (key))) {
      _keys.add (key)
    }

    let newMap = new _Map ()
    newMap._map = _map
    newMap._keys = _keys
    return newMap
  }

  remove (key) {
    let _map = Object.assign ({}, this._map)
    delete _map [_hash (key)]

    let _keys = new Set (this._keys)
    _keys.delete (key)

    let newMap = new _Map ()
    newMap._map = _map
    newMap._keys = _keys
    return newMap
  }

  setNth (key, value) {
    this._map [_hash (key)] = value
    if (!this._map.hasOwnProperty (_hash (key))) {
      this._keys.add (key)
    }

    return this
  }

  keys () {
    let keys = new ListEmpty ()
    for (let key of this._keys) {
      keys = new List (key, keys)
    }
    return keys
  }

  // Return keys as mutable array
  // TODO: Reverse?
  keysMut () {
    return [...this._keys]
  }

  // Use Set.size?
  isEmpty () {
    return this._keys.size === 0
  }

  eq (other) {
    if (this.type !== other.type)
      return false
    if (this._keys.size !== other._keys.size)
      return false

    // Optimize (remove call to _hash, use hasOwnProperty?)
    for (let x of this._keys)
      if (typeof other._map[_hash (x)] === "undefined")
        return false

    for (let key in this._map) {
      if (!eq(this._map[key], other._map[key]))
        return false
    }
    return true
  }

  toString () {
    let keys = this.keysMut ()
    let pairs = []
    for (let key of keys) {
      let value = this._map [_hash (key)]
      pairs.push (toStr (key) + " " + toStr (value))
    }
    return "{" + pairs.join (" ") + "}"
  }

  printToString () {
    let keys = this.keysMut ()
    let pairs = []
    for (let key of keys) {
      let value = this._map [_hash (key)]
      pairs.push (printToStr (key) + " " + printToStr (value))
    }
    return "{" + pairs.join (" ") + "}"
  }


  hash () {
    return 0
  }

  emptyOf () {
    return new _Map ()
  }

  toJS () {
    let object = {}
    this._keys.forEach (key => {
      object[toJS (key)] = toJS (this._map [_hash (key)])
    })
    return object
  }
}

// String
String.prototype.type = "String"
String.prototype.isSeq = true

String.prototype.first = function () {
  return new Char (this.charAt (0))
}

String.prototype.rest = function () {
  return new StringIterator (this, 1)
}

String.prototype.prepend = function (char) {
  return char._chr + this
}

String.prototype.isEmpty = function () {
  return this.length === 0
}

String.prototype.len = function () {
  return this.length
}

String.prototype.nth = function (index) {
  return new Char (this.charAt (index))
}

String.prototype.emptyOf = function () {
  return ""
}

String.prototype.printToStr = function () {
  return "\"" + this.split ("\"").join ("\\\"") + "\""
}

// Vector
Array.prototype.type = "Vector"
Array.prototype.isSeq = true

Array.prototype.first = function () {
  return this[0]
}

Array.prototype.rest = function () {
  return this.slice (1)
}

Array.prototype.isEmpty = function () {
  return this.length === 0
}

Array.prototype.prepend = function (item) {
  let newArray = [item]
  for (let it = 0; it < this.length; it++) {
    newArray.push (this[it])
  }
  return newArray
}

Array.prototype.nth = function (index) {
  return this[index]
}

Array.prototype.len = function () {
  return this.length
}

Array.prototype.eq = function (other) {
  if (other.type !== "Vector")
    return false

  for (let it = 0; it < this.length && it < other.length; it++) {
    if (!eq (this[it], other[it])) {
      return false
    }
  }
  return true
}

Array.prototype.emptyOf = function () {
  return []
}

Array.prototype.toString = function () {
  return "[| " + this.map (x => x.toString ()).join (" ") + " |]"
}

Array.prototype.printToString = function () {
  return "[| " + this.map (x => printToStr (x)).join (" ") + " |]"
}

Array.prototype.toVector = function () {
  return this
}

// Module
class Module {
  constructor (exports) {
    this.exports = exports
  }

  nth (x) {
    return this.exports[x._id]
  }
}

// StringIterator

class StringIterator {
  constructor (str, index) {
    this._str = str
    this._index = index
  }

  nth (x) {
    return new Char (this._str.charAt (this._index + x))
  }

  first () {
    return new Char (this._str.charAt (this._index))
  }

  rest () {
    return new StringIterator (this._str, this._index + 1)
  }

  len () {
    return this._str.length - this._index
  }

  isEmpty () {
    return this._str.length === this._index
  }

  prepend (char) {
    return char._chr + this._str.substr (this._index)
  }

  eq (other) {
    return eq (this._str.substr (this._index), other)
  }

  toString () {
    return this._str.substr (this._index)
  }

  printToString () {
    return "\"" + this._str.substr (this._index) + "\""
  }

  emptyOf () {
    return ""
  }
}

const globalScope = this
class JSNamespace {
  constructor () {}
  nth (x) {
    return globalScope[x.toString ()]
  }
}

Object.prototype.nth = function (index) {
  return this[index.toString ()]
}
