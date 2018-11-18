# Language

A functional programming language.

```clojure
(print "Hello, World!")
```

### Features
- First-Class Functions & Closures
- Immutable Data Structures
- Dynamic Type System
- Macro System (only supported by self-hosted compiler)

### Example

**Factorial:**
```clojure
(defn fact [x]
  (if (= x 1)
    1
    (* (fact (decr x)) x)))

(print (fact 4))
```

### Installation
```bash
$ git clone <url> <name>
```

To compile a file:
```bash
$ python3 src/compiler_py/main.py <filename>
```

### Learning

- **Getting Started:** doc/getting-started/getting-started.md

##### Documentation

- **Various Examples:** doc/examples
- **Standart Library Documentation:** doc/lib (TODO)

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
  - **lib**: Standart Library Documentation
- **lib**: The standart library
- **src**
  - **compiler**: Self-Hosted implementation of the compiler
    - **runtime**: Runtimes for the different compilation targets
  - **compiler_py**: Messy compiler prototype written in python
- **test**: Unit Tests for the standart library
  - **misc**: Other tests
    - **speed**: Simple files to test the speed of the language
