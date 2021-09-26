# godot-parser-generator

### What is this?

A tool that generates parsers for Godot, based on [alexpizarroj/lalr1-table-generator](https://github.com/alexpizarroj/lalr1-table-generator),
that I made because I needed a GLSL parser for [Material Maker](https://github.com/RodZill4/material-maker).

### How to use it?

First you'll need a grammar in a text file (see glsl_grammar.txt for the format).

Just run the following command:

 python generate.py <grammar-file> <output-gd-file>
 
You will have to edit the generated file to:
- make sure it inherits parser_base.gd in your Godot project (update the part to that file)
- solve conflicts in the generated table (search for the "conflict" string)
- create a new script that inherits the generated script and implements the lexer (see GLSL parser in
  [Material Maker](https://github.com/RodZill4/material-maker) as an example), and functions to
  generate the AST you want (a default AST that packs all tokens will be generated if you don't).
