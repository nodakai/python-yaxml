import xml.etree.ElementTree as ET

import yaxml


def test_validate():
    assert yaxml.validate('<foo/>', '''
<element name="foo" xmlns="http://relaxng.org/ns/structure/1.0" >
<empty/>
</element>
        ''')

    assert yaxml.validate(yaxml.relaxng_in_relaxng.DATA,
                          yaxml.relaxng_in_relaxng.DATA)


def test_load_yaml_as_xml():
    xml = yaxml.load_yaml_as_xml('''
Root:
    Foo:
        Bar:
            _baz: 1
            _quux: true
    ''')
    assert (
        '<Root><Foo><Bar _baz="1" _quux="true" /></Foo></Root>' == ET.tostring(
            xml.getroot(), 'unicode'))


def test_load_rngyaml_0():
    y = yaxml.load_rngyaml('''
schema:
    addressBook: true
    ''')
    assert {
        'element': 'element',
        'name': 'addressBook',
        'child': {
            'element': 'text',
        }
    } == y

def test_load_rngyaml_1():
    y = yaxml.load_rngyaml('''
schema:
    addressBook:
        - name: true
        - email: true
    ''')

    y0 = y.pop('child')
    assert {
        'element': 'element',
        'name': 'addressBook'
    } == y

    y1, y2 = y0
    assert {
        'element': 'element',
        'name': 'name',
        'child': {
            'element': 'text'
        }
    } == y1
    assert {
        'element': 'element',
        'name': 'email',
        'child': {
            'element': 'text'
        }
    } == y2

def test_load_rngyaml_2():
    y = yaxml.load_rngyaml('''
schema:
    addressBook:
        card*:
            - name: true
            - email: true
    ''')

    y0 = y.pop('child')
    assert {
        'element': 'element',
        'name': 'addressBook'
    } == y

    y1 = y0.pop('child')
    assert {
        'element': 'zeroOrMore',
    } == y0

    y2 = y1.pop('child')
    assert {
        'element': 'element',
        'name': 'card'
    } == y1

    y3, y4 = y2
    assert {
        'element': 'element',
        'name': 'name',
        'child': {
            'element': 'text'
        }
    } == y3
    assert {
        'element': 'element',
        'name': 'email',
        'child': {
            'element': 'text'
        }
    } == y4
