import xml.etree.ElementTree as ET
import xml.dom.minidom as dom
from pprint import pprint as pp, pformat as pf

import yaxml


def xmlpp(xmlstr):
    return dom.parseString(xmlstr).toprettyxml(indent="  ", newl="\n")


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


SIMPLE = '''
schema:
    addressBook: true
'''


def load_rngyaml(s):
    # disable automatic validation
    return yaxml.load_rngyaml(s, False)


def test_load_rngyaml_simple():
    y = load_rngyaml(SIMPLE)

    assert {
        'element': 'element',
        'name': 'addressBook',
        'child': {
            'element': 'text',
        }
    } == y


ELEM_SEQ_0 = '''
schema:
    addressBook:
        - name: true
        - name: true
'''


def test_load_rngyaml_elem_seq_0():
    y = load_rngyaml(ELEM_SEQ_0)

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
        'name': 'name',
        'child': {
            'element': 'text'
        }
    } == y2


ELEM_SEQ_1 = '''
schema:
    addressBook:
        - name: true
        - email: true
'''


def test_load_rngyaml_elem_seq_1():
    y = load_rngyaml(ELEM_SEQ_1)

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


ELEM_DIC = '''
schema:
    addressBook:
        name: true
        email: true
'''


def test_load_rngyaml_elem_dic():
    y = load_rngyaml(ELEM_DIC)

    y0 = y.pop('child')
    assert {
        'element': 'element',
        'name': 'addressBook'
    } == y

    y1 = y0.pop('child')
    assert {
        'element': 'interleave'
    } == y0

    y2, y3 = y1
    if y2['name'] != 'name':
        y2, y3 = y3, y2

    assert {
        'element': 'element',
        'name': 'name',
        'child': {
            'element': 'text'
        }
    } == y2

    assert {
        'element': 'element',
        'name': 'email',
        'child': {
            'element': 'text'
        }
    } == y3


ZERO_OR_MORE = '''
schema:
    r:
        a*:
            p: true
        b*:
            q: true
'''


def test_load_rngyaml_zero_or_more():
    y = load_rngyaml(ZERO_OR_MORE)

    y0 = y.pop('child')
    assert {
        'element': 'element',
        'name': 'r'
    } == y

    y1 = y0.pop('child')
    assert {
        'element': 'interleave',
    } == y0

    y2, y3 = y1
    if y2['child']['name'] == 'b':
        y2, y3 = y3, y2

    y20 = y2.pop('child')
    assert {
        'element': 'zeroOrMore',
    } == y2

    y21 = y20.pop('child')
    assert {
        'element': 'element',
        'name': 'a'
    } == y20

    assert {
        'element': 'element',
        'name': 'p',
        'child': {
            'element': 'text'
        }
    } == y21

    y30 = y3.pop('child')
    assert {
        'element': 'zeroOrMore',
    } == y3

    y31 = y30.pop('child')
    assert {
        'element': 'element',
        'name': 'b'
    } == y30

    assert {
        'element': 'element',
        'name': 'q',
        'child': {
            'element': 'text'
        }
    } == y31


ONE_ATTR_ONLY = '''
schema:
    rr:
        _aa: true
'''


def test_load_rngyaml_one_attr_only():
    y = load_rngyaml(ONE_ATTR_ONLY)

    y0 = y.pop('child')
    assert {
        'element': 'element',
        'name': 'rr'
    } == y

    assert {
        'element': 'attribute',
        'name': 'aa',
        'child': {
            'element': 'text'
        }
    } == y0


ATTR_ONLY = '''
schema:
    r0:
        _a0: true
        _b0: true
'''


def test_load_rngyaml_attr_only():
    y = load_rngyaml(ATTR_ONLY)

    y0 = y.pop('child')
    assert {
        'element': 'element',
        'name': 'r0'
    } == y

    y1, y2 = y0
    if y1['name'] == 'b0':
        y1, y2 = y2, y1

    assert {
        'element': 'attribute',
        'name': 'a0',
        'child': {
            'element': 'text'
        }
    } == y1

    assert {
        'element': 'attribute',
        'name': 'b0',
        'child': {
            'element': 'text'
        }
    } == y2


ATTR_ONLY_ARR = '''
schema:
    r1:
        - _a1: true
        - _b1: true
'''


def test_load_rngyaml_attr_only_arr():
    y = load_rngyaml(ATTR_ONLY_ARR)

    y0 = y.pop('child')
    assert {
        'element': 'element',
        'name': 'r1'
    } == y

    y1, y2 = y0
    if y1['name'] == 'b1':
        y1, y2 = y2, y1

    assert {
        'element': 'attribute',
        'name': 'a1',
        'child': {
            'element': 'text'
        }
    } == y1

    assert {
        'element': 'attribute',
        'name': 'b1',
        'child': {
            'element': 'text'
        }
    } == y2


ESCAPED_0 = '''
schema:
    r2:
        $element:
            e: true
'''


def test_load_rngyaml_escaped_0():
    y = load_rngyaml(ESCAPED_0)

    y0 = y.pop('child')
    assert {
        'element': 'element',
        'name': 'r2'
    } == y

    assert {
        'element': 'element',
        'name': 'e',
        'child': {
            'element': 'text'
        }
    } == y0


ESCAPED_1 = '''
schema:
    r3:
        - $element:
            e3: true
'''


def test_load_rngyaml_escaped_1():
    y = load_rngyaml(ESCAPED_1)

    y0 = y.pop('child')
    assert {
        'element': 'element',
        'name': 'r3'
    } == y

    assert [{
        'element': 'element',
        'name': 'e3',
        'child': {
            'element': 'text'
        }
    }] == y0


ESCAPED_2 = '''
schema:
    r4:
        - $element:
            e4: true
        - $element:
            e4: true
'''


def test_load_rngyaml_escaped_2():
    y = load_rngyaml(ESCAPED_2)

    y0 = y.pop('child')
    assert {
        'element': 'element',
        'name': 'r4'
    } == y

    y1, y2 = y0

    assert {
        'element': 'element',
        'name': 'e4',
        'child': {
            'element': 'text'
        }
    } == y1

    assert {
        'element': 'element',
        'name': 'e4',
        'child': {
            'element': 'text'
        }
    } == y2


ESCAPED_ATTR_0 = '''
schema:
    r5:
        $attribute:
            a: true
'''


def test_load_rngyaml_escaped_attr_0():
    y = load_rngyaml(ESCAPED_ATTR_0)

    y0 = y.pop('child')
    assert {
        'element': 'element',
        'name': 'r5'
    } == y

    assert {
        'element': 'attribute',
        'name': 'a',
        'child': {
            'element': 'text'
        }
    } == y0


ESCAPED_ATTR_1 = '''
schema:
    r6:
        - $attribute:
            a: true
'''


def test_load_rngyaml_escaped_attr_1():
    y = load_rngyaml(ESCAPED_ATTR_1)

    y0 = y.pop('child')
    assert {
        'element': 'element',
        'name': 'r6'
    } == y

    assert [{
        'element': 'attribute',
        'name': 'a',
        'child': {
            'element': 'text'
        }
    }] == y0


ESCAPED_ATTR_2 = '''
schema:
    r7:
        $attribute:
            a: true
        _b: true
'''


def test_load_rngyaml_escaped_attr_2():
    y = load_rngyaml(ESCAPED_ATTR_2)

    y0 = y.pop('child')
    assert {
        'element': 'element',
        'name': 'r7'
    } == y

    y1, y2 = y0
    if y1['name'] == 'b':
        y1, y2 = y2, y1

    assert {
        'element': 'attribute',
        'name': 'a',
        'child': {
            'element': 'text'
        }
    } == y1

    assert {
        'element': 'attribute',
        'name': 'b',
        'child': {
            'element': 'text'
        }
    } == y2


ESCAPED_ATTR_3 = '''
schema:
    r8:
        - card*:
            _name: true
            $attribute:
                email: true
        - $element:
            e: true
        - $element:
            _e: true
        - $element:
            __e: true
        - $element:
            e:
                e: true
'''


def test_load_rngyaml_escaped_attr_3():
    y = load_rngyaml(ESCAPED_ATTR_3)

    y0 = y.pop('child')
    assert {
        'element': 'element',
        'name': 'r8'
    } == y

    y1, y2, y3, y4, y5 = y0

    y10 = y1.pop('child')
    assert {
        'element': 'zeroOrMore',
    } == y1

    y11 = y10.pop('child')
    assert {
        'element': 'element',
        'name': 'card'
    } == y10

    y12, y13 = y11
    if y12['name'] == 'email':
        y12, y13 = y13, y12

    assert {
        'element': 'attribute',
        'name': 'name',
        'child': {
            'element': 'text'
        }
    } == y12

    assert {
        'element': 'attribute',
        'name': 'email',
        'child': {
            'element': 'text'
        }
    } == y13

    assert {
        'element': 'element',
        'name': 'e',
        'child': {
            'element': 'text'
        }
    } == y2

    assert {
        'element': 'element',
        'name': '_e',
        'child': {
            'element': 'text'
        }
    } == y3

    assert {
        'element': 'element',
        'name': '__e',
        'child': {
            'element': 'text'
        }
    } == y4

    assert {
        'element': 'element',
        'name': 'e',
        'child': {
            'element': 'element',
            'name': 'e',
            'child': {
                'element': 'text'
            }
        }
    } == y5


def test_compile_rngyaml_to_rng():
    def f(y):
        internal = load_rngyaml(y)
        xmlstr = ET.tostring(yaxml.compile_rngyaml_to_rng(internal), 'unicode')
        pped = xmlpp(xmlstr)
        rc, err = yaxml.run_validator(pped, yaxml.relaxng_in_relaxng.DATA)
        return (0 == rc, err + '\n' + pf(internal) + '\n' + pped)

    ok, err = f(SIMPLE)
    assert ok, err
    ok, err = f(ELEM_SEQ_0)
    assert ok, err
    ok, err = f(ELEM_SEQ_1)
    assert ok, err
    ok, err = f(ELEM_DIC)
    assert ok, err
    ok, err = f(ZERO_OR_MORE)
    assert ok, err
    ok, err = f(ONE_ATTR_ONLY)
    assert ok, err
    ok, err = f(ATTR_ONLY)
    assert ok, err
    ok, err = f(ATTR_ONLY_ARR)
    assert ok, err
    ok, err = f(ESCAPED_0)
    assert ok, err
    ok, err = f(ESCAPED_1)
    assert ok, err
    ok, err = f(ESCAPED_2)
    assert ok, err
    ok, err = f(ESCAPED_ATTR_0)
    assert ok, err
    ok, err = f(ESCAPED_ATTR_1)
    assert ok, err
    ok, err = f(ESCAPED_ATTR_2)
    assert ok, err
    ok, err = f(ESCAPED_ATTR_3)
    assert ok, err
#   ok, err = f(ESCAPED_3)
#   assert ok, err
