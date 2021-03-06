# Language

A functional programming language.

```clojure
(print "Hello, world!")
```

### Features
- First-Class Functions & Closures
- Immutable Data Structures
- Dynamic Type System
- Macro System

### Example

**Factorial:**
```clojure
(defn fact [x]
  (if (= x 0)
    1
    (* (fact (decr x)) x)))

(print (fact 4))
```

### Installation
```bash
$ git clone https://github.com/pseudo-random/lang lang
$ cd lang
$ bash build.sh
```

To compile a file:
```bash
$ node compile.js path/to/file.txt
```

### Learning

- **Getting Started:** [doc/getting-started/getting-started.md](https://github.com/pseudo-random/lang/blob/master/doc/getting-started/getting-started.md)

##### Documentation

- **Various Examples:** doc/examples
- **Standard Library Documentation:** doc/lib (TODO)

##### Tutorials

- TODO

### Contribute
Contributions are welcome. There are a few different ways to contribute:
- Filing Bug Reports
- Improving/Writing Documentation
- Creating Tutorials
- Submitting Examples
- Creating Libraries
- Contributing Code

Just remember to be nice.

**Note:** Consider opening an issue to discuss *new features* before implementing them.

###### Project Structure

- **doc**: Documentation
  - **examples**: Various Examples
  - **getting-started**: "Getting Started" Tutorial
  - **lib**: Standard Library Documentation
- **lib**: The standard library
- **src**
  - **compiler**: Self-Hosted implementation of the compiler
    - **runtime**: Runtimes for the different compilation targets
  - **compiler_py**: Messy compiler prototype written in python
- **test**: Unit Tests for the standard library
  - **misc**: Other tests
    - **speed**: Simple files to test the speed of the language
