# YaXML

Author: NODA, Kai <nodakai@gmail.com>

Homepage: https://github.com/nodakai/python-yaxml

## YAML-to-XML converter in Python, with a handy RELAX NG interfacing

*Very* experimental, covers only ~10 % of the relevant specs

This software was written primarily for "XML as a config format."

Huge documents like OOXML are/will not be in the scope.

In particular, it does not support mixture of text and child elements like this:

    <foo>abc<bar>def<baz/>ghi</bar>jkl</foo>

* [YAML 1.2][yaml]
* [RELAX NG][rng]

## Usage

Quoted from [`test_0.py`](https://github.com/nodakai/python-yaxml/blob/master/yaxml/test_0.py):

```python
xml = yaxml.load_yaml_as_xml('''
Root:
    Foo:
        Bar:
            _baz: 1
            _quux: true
''')
assert (
    '<Root><Foo><Bar baz="1" quux="true" /></Foo></Root>' == ET.tostring(
        xml.getroot(), 'unicode'))
```

The documantation is almost entirely missing.
Meanwhiile you can take a look into the test file to get the idea on how it's supposed to work.

## RngYaml: RELAX NG expressed in YAML

Again, quoted from the unit test:

```python
ZERO_OR_MORE = '''
schema:
    r:
        a*:
            p: true
        b*:
            q: true
'''

y = load_rngyaml(ZERO_OR_MORE)
x = compile_rngyaml_to_rng(y)
```

The output `x` is a RELAX NG schema which you can feed to tools such as [`xmllint(1)`][xmllint]:

```xml
<?xml version="1.0" ?>
<element name="r" xmlns="http://relaxng.org/ns/structure/1.0">
  <interleave>
    <zeroOrMore>
      <element name="b">
        <element name="q">
          <text/>
        </element>
      </element>
    </zeroOrMore>
    <zeroOrMore>
      <element name="a">
        <element name="p">
          <text/>
        </element>
      </element>
    </zeroOrMore>
  </interleave>
</element>
```

You can think this of as a variant of [RELAX NG Compact Syntax][rnc].

[yaml]: http://yaml.org/
[rng]: http://relaxng.org/
[rnc]: http://relaxng.org/compact-tutorial.html
[xmllint]: http://xmlsoft.org/xmllint.html
