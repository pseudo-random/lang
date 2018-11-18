#include <iostream>

class var;
class cons;
class str {
public:
  str (char c, str* r) : chr (c), rest (r) {}
  bool isEmpty () { return rest == nullptr; }
  void write () {
    str* cur = this;
    while (cur != nullptr) {
      std::cout << cur->chr;
      cur = cur->rest;
    }
  }

  char chr;
  str* rest = nullptr;
};

class fn {
public:
  virtual var call (int argc, var* argv) = 0;
};

#define TYPE_INT 0
#define TYPE_FLOAT 1
#define TYPE_BOOL 2
#define TYPE_LIST 3
#define TYPE_STR 4
#define TYPE_ARRAY 5
#define TYPE_CHAR 6
#define TYPE_SYMBOL 7
#define TYPE_NIL 8
#define TYPE_VECTOR 9
#define TYPE_TYPE 10
#define TYPE_FN 11

class var {
public:
  var () : type (TYPE_NIL) {}
  var (int value) : type (TYPE_INT) { val.Int = value; }
  var (double value) : type (TYPE_FLOAT) { val.Float = value; }
  var (bool value) : type (TYPE_BOOL) { val.Bool = value; }
  var (cons* value) : type (TYPE_LIST) { val.List = value; }
  var (str* value) : type (TYPE_STR) { val.Str = value; }
  var (int len, char* string) : type (TYPE_STR) {
    str* cur = nullptr;
    for (int it = len-1; it >= 0; it--) {
      cur = new str (string[it], cur);
    }
    val.Str = cur;
  }
  var (fn* func) : type (TYPE_FN) { val.Fn = func; }

  var operator+ (const var& other) {
    if (type == TYPE_INT && other.type == TYPE_INT)
      return var (val.Int + other.val.Int);
    if (type == TYPE_FLOAT && other.type == TYPE_FLOAT)
      return var (val.Float + other.val.Float);
    return var ();
  }

  var operator- (const var& other) {
    if (type == TYPE_INT && other.type == TYPE_INT)
      return var (val.Int - other.val.Int);
    if (type == TYPE_FLOAT && other.type == TYPE_FLOAT)
      return var (val.Float - other.val.Float);
    return var ();
  }

  var operator== (const var& other) {
    if (type == TYPE_INT && other.type == TYPE_INT)
      return val.Int == other.val.Int;
  }

  var write () {
    switch (type) {
      case TYPE_STR: val.Str->write (); break;
      case TYPE_INT: std::cout << val.Int; break;
      case TYPE_FLOAT: std::cout << val.Float; break;
      case TYPE_BOOL: std::cout << val.Bool; break;
      case TYPE_NIL: std::cout << "nil"; break;
      default: std::cout << "<UNKNOWN_TYPE>";
    }

    return var ();
  }

  var print () {
    write ();
    std::cout << std::endl;
    return var ();
  }

  var operator() (int argc, var* argv) {
    return val.Fn->call (argc, argv);
  }

  var operator() () { return val.Fn->call (0, nullptr); }
  var operator() (var a) { var args[] = {a}; return val.Fn->call (1, args); }
  var operator() (var a, var b) { var args[] = {a, b}; return val.Fn->call (2, args); }
  var operator() (var a, var b, var c) { var args[] = {a, b, c}; return val.Fn->call (3, args); }

  // Helper Functions
  bool isNumber () { return type == TYPE_INT || type == TYPE_FLOAT; }
  fn* getFn () { /* check? */ return val.Fn; }

private:
  union {
    int Int;
    double Float;
    bool Bool;
    cons* List;
    str* Str;
    str* Char; // TODO: SimpleChar and Char types
    int Symbol;
    fn* Fn;
  } val;
  int type;
};

class cons {
public:
  cons (const var& f, cons* r) : first (f), rest (r) {}
  bool isEmpty () { return rest == nullptr; }

  var first;
  cons* rest = nullptr;
};

class test_fn : public fn {
public:
  test_fn (var d) : delimiter (d) {
  }

  var call (int argc, var* argv) {
    for (int it = 0; it < argc-1; it++) {
      argv[it].write ();
      delimiter.write ();
    }
    argv[argc-1].print ();

    return var ();
  }
private:
  var delimiter;
};

int main () {
  char str_0[] = "Hello, world!";
  var my_str (sizeof(str_0)-1, str_0);
  my_str.write ();
  my_str.print ();

  var a (2);
  var b (3);
  var c = (a + b);
  c.print ();

  char str_1[] = " ";
  var my_test_fn (new test_fn (var (sizeof (str_1) -1, str_1)));
  //my_test_fn.getFn ()->closure (var (sizeof (str_1) -1, str_1));
  my_test_fn (a, b);
  my_test_fn (a, b, c);

  return 0;
}
