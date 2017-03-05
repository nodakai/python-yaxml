from copy import deepcopy as dcp
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


Y0 = yaxml.load_rngyaml('''
schema:
    addressBook: true
''')


def test_load_rngyaml_0():
    y = dcp(Y0)

    assert {
        'element': 'element',
        'name': 'addressBook',
        'child': {
            'element': 'text',
        }
    } == y


Y1 = yaxml.load_rngyaml('''
schema:
    addressBook:
        - name: true
        - email: true
''')


def test_load_rngyaml_1():
    y = dcp(Y1)

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


Y2 = yaxml.load_rngyaml('''
schema:
    addressBook:
        card*:
            - name: true
            - email: true
''')


def test_load_rngyaml_2():
    y = dcp(Y2)

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


def test_compile_rngyaml_to_rng():
    def f(y):
        s = ET.tostring(yaxml.compile_rngyaml_to_rng(dcp(y)), 'unicode')
        return yaxml.validate(s, yaxml.relaxng_in_relaxng.DATA)

    assert f(Y0)
    assert f(Y1)
    assert f(Y2)
