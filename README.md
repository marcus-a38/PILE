# P . I . L . E - Python Interpretive Lexical Evaluator

Operates very similar to the Python interpreter (built in Python!) but with simple, powerful customization in the palm of your hands. Tailor your microlanguage to your desired settings, and watch as your personal interpreter provides the desired results, with minimized overhead.
___

Table of Contents:

1. [Configuration](#configuration)
2. [Lexing and Tokenization](#lexing-and-tokenization)
3. [Parsing and AST Generation](#parsing-and-ast-generation)
4. [Compilation](#compilation)
5. [Interpreting](#interpreting)

___

## Configuration

### Pile Config Syntax

P.I.L.E GUI and P.I.L.E Terminal utilize configuration files or streams to define the syntax and structure of your microlanguage. These configuration inputs follow a P.I.L.E specific metalanguage (simply referred to as Pile, or Pile Form to avoid confusion.) Below is a complete glossary and documentation of Pile Form syntax:

### Do's and Dont's

When configuring your P.I.L.E software, there's a few things that should be avoided:



___

## Lexing and Tokenization

### Logic

P.I.L.E follows a standard approach to lexing and tokenization, applying regular expressions to match and name strings in the input stream. Regular expressions are incredibly sensitive, and can be confusing for beginners, so make sure you craft each regular expression with plenty of forethought. Fortunately, however, Pile Form greatly simplifies the pattern creation process-- the configparser module and regex generator will break down your Pile Form representations, and build a proper pattern.

The tokenization process is fairly straightforward. First, a Lexer instance is initialized, which contains the public method 'lex'. This method is the entry point to tokenization, and it returns a list of generators for each line. Every iteration over the line generator will produce one unique Token instance, containing the raw value of the token, the token type, the location of the token on the source file, and a string representation of the token.

The use of generators here is entirely intentional, and potentially necessary in specific cases where the input size is mammoth. Each token should be accessed programmatically, to limit overhead in tokenization.

### Potential for Parallelization

As mentioned, tokenization has incredible, potential performance flaws when met with large inputs. I theorize that I can take tokenization a step further, and I can thread the Lexer methods for those outlying issues. This is just conceptual at this point. It may be better to make this optional, depending on the specific constraints on your language.

### External Use Cases

P.I.L.E can be imported and used as a framework. The Lexer, Token, and REPatterns classes (plus their methods) can be incredibly useful for quick lexical analysis implementation. Some examples of where this can be applied are: syntax highlighting, data extraction, NLP, web scraping, and more!

You can get a customized Lexer up and running with just a few lines of code:

```python

from lex.lexer import *

patterns = [({FOO}, {BAR}), ({EGGS}, {SPAM}), ( ... )]
my_input = ["Lorem", "ipsum", ...]

lexer_ = Lexer()
lexer_.re_patterns = REPatterns(args=patterns)
lexer_.lex(my_input)

for line in lexer_.lex_list:
  for token in line:
    
...

```

**NOTE**: This will be changed relatively soon, as the args in Lexer will *actually* have purpose (in providing custom patterns).

___

## Parsing and AST Generation

### SECTIONS TO ADD:

### Parsing Logic

### Abstract Syntax

### AST Generation

### Node Manipulation

### External Use Cases

___

## Compilation

### SECTIONS TO ADD:

### Looking at Bytecode

### Memory Management

___

## Interpreting

### SECTIONS TO ADD:

### Reading the Bytecode

### Execution

___

## Usage

### SECTIONS TO ADD:

### Guide by Operating System

### As an Import

### Use Cases (Cummulative)

