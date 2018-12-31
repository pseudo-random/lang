# Getting Started

```clojure
(print "Hello, World!") ; output: Hello, World!
```

### Math

```clojure
(+ 2 3) ; => 5
(- 5 3) ; => 2
(* 2 3) ; => 6
(/ 6 2) ; => 3
(% 7 5) ; => 2

(incr 1) ; => 2
(decr 1) ; => 0
(sign 10) ; => 1
(sign 0) ; => 0
(sign -10) ; => -1

(sqrt 4) ; => 2
```

### Definitions
`(def name value)`

```clojure
(def x 10)
(print (+ x x)) ; output: 20
```

###### let
`(let bindings & body)`

```clojure
(let [x 10]
  (print (+ x x))) ; output: 20
```

### If
`(if condition then else)`

```clojure
(if (= 1 2)
  (print "Yes")
  (print "No"))
; output: No
```

###### Cond
`(cond & condition then)`

```clojure
(def x 3)
(cond
  (= x 1) "one"
  (= x 2) "two"
  (= x 3) "three"
  :else   "?") ; => "three"
```

###### When
`(when condition & body)`

###### Unless
`(unless condition & body)`

### Functions
`(fn parameters & body)`

```clojure
(def add-one (fn [x]
  (+ x 1)))

(print (add-one 3)) ; output: 4
```

`(defn name parameters & body)`

```clojure
(defn add-one [x]
  (+ x 1)))

(print (add-one 3)) ; output: 4
```

###### recur
```clojure
(defn print-inf [text]
  (print text)
  (recur text))

(print-inf "Hello, World!")
; output:
;    Hello, World!
;    Hello, World!
;    Hello, World!
;    ...
```

**Note:** You can interrupt the program using Ctrl+C

### Example
###### Prime?
```clojure
(defn prime? [x]
  (defn prime' [div]
    (cond
      (= div 1)    true
      (div? x div) false
      :else        (recur (decr div))))
  (if (> x 0)
    (prime' (decr x))
    false))
```

### Seqs
###### List
```clojure
(def my-list (quote (1 2 3 4 5)))  ; Create a list using quote
(def my-list-2 [1 2 3 4 5]) ; Create a list using brackets

(first my-list) ; => 1
(rest my-list) ; => (2 3 4 5)
(prepend my-list 0) ; => (0 1 2 3 4 5)
(append my-list 6) ; => (1 2 3 4 5 6)
(empty? my-list) ; => false
(empty? []) ; => true

(second my-list) ; => 2
(third my-list) ; => 3
```

###### Map, Filter, Reduce
```clojure
(def my-list (range 1 5))
my-list ; => (1 2 3 4)

(map my-list incr) ; => (2 3 4 5)
(filter my-list even?) ; => (2 4)
(reject my-list even?) ; => (1 3)
(reduce my-list +) ; => 10

(each my-list print)
; output:
;    1
;    2
;    3
;    4
```

###### Drop, Take, Split-At, Zip
```clojure
(drop [1 2 3 4] 2) ; => (3 4)
(take [1 2 3 4] 2) ; => (1 2)

(split-at [1 2 3 4] 2) ; => ((1 2) (3 4))

(zip [1 2 3] [4 5 6]) ; => ((1 4) (2 5) (3 6))
```

###### In?, Reshape-Width
```clojure
(in? 1 [1 2 3]) ; => true
(in? 0 [1 2 3]) ; => false

(reshape-width (range 1 10) 3) ; => ((1 2 3) (4 5 6) (7 8 9))
```

###### String
```clojure
(def str "abc")
(print str) ; output: abc

(first "abc") ; => \a
(rest "abc") ; => "bc"
(concat "abc" "def") ; => "abcdef"
(interpose ["A" "B" "C"] ", ") ; => "A, B, C"

(format "1 + 2 = " (+ 1 2)) ; => "1 + 2 = 3"
```

### Modules

`(import module-name)`

```clojure
(import random)

(random/randint! 0 10)
; => Random int between 0 (inclusive) and 10 (exclusive)
```

###### Unit Testing
`(test name & res operator expected)`

```clojure
(import test)

(test/test "Some Test"
  (+ 1 2) = 3
  (+ 3 4) = 7)
```

###### File IO

```clojure
(import io)
(io/write! ["my-file.txt"] "Hello, world!" "utf-8")
(print (io/read! ["my-file.txt"] "utf-8"))
```
