# YaXML

Author: NODA, Kai <nodakai@gmail.com>

Homepage: https://github.com/nodakai/python-yaxml

## YAML-to-XML converter in Python, with a handy RELAX NG interfacing

*Very* experimental, covers only ~10 % of the relevant specs

This software was written primarily for "XML as a config format."

Huge documents like OOXML are/will not be in the scope.

In particular, it does not support mixture of text and child elements like this:

    <foo>abc<bar>def<baz/>ghi</bar>jkl</foo>
