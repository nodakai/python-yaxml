import os
import os.path
import tempfile
import subprocess
import numbers
import pprint
import xml.etree.ElementTree as ET

import yaml as pyyaml

from . import relaxng_in_relaxng


def abbrev(source):
    '''
    >>> abbrev('01234567890123456789012')
    '01234567890123456789012'
    >>> abbrev('0123456789012345678901234')
    '0123456789...5678901234'
    '''

    N = 10
    return source if len(source) <= 2 * N + 3 else source[ :N] + '...' + source[-N: ]


class Exc(Exception):
    def __init__(self, fmt, *args):
        super(Exc, self).__init__(fmt.format(*args))


class RngYamlParseError(Exc):
    def __init__(self, fmt, *args):
        super(RngYamlParseError, self).__init__(fmt, *args)


MODIFIERS = [ 'zeroOrMore', 'oneOrMore', 'optional' ]
MODIFIERS_D = dict(p for p in zip(['*', '+', '?'], MODIFIERS))


class RngYamlParser(object):
    def __init__(self, prefix):
        self._prefix = prefix
        self._extra_checks = []

    def parse_pattern(self, path, y):  # I know it's very complex # noqa: C901
        if isinstance(y, dict):
            for k, v in y.items():
                if self._prefix + 'attribute' == k:
                    pass
                elif self._prefix + 'interleave' == k:
                    pass
                elif self._prefix + 'choice' == k:
                    pass
                elif self._prefix + 'optional' == k:
                    pass
                elif self._prefix + 'list' == k:
                    pass
                elif self._prefix + 'mixed' == k:
                    pass
                elif self._prefix + 'ref' == k:
                    pass
                elif self._prefix + 'parentRef' == k:
                    pass
                elif self._prefix + 'value' == k:
                    pass
                elif self._prefix + 'data' == k:
                    pass
                elif self._prefix + 'notAllowed' == k:
                    pass
                elif self._prefix + 'externalRef' == k:
                    pass
                elif self._prefix + 'grammar' == k:
                    pass
                else:
                    return self.parse_element(path, k, v)
        elif isinstance(y, list):
            return [ self.parse_pattern(path, e) for e in y ]
        elif is_scalar(y):
            return self.parse_text(path, y)
        else:
            raise Exception("{}: what is {}".format(path, pprint.pformat(y)))

    def parse_element(self, path, name, val):
        mod = MODIFIERS_D.get(name[-1: ])
        if mod:
            realname = name[ :-1]
        else:
            realname = name

        child = self.parse_pattern(path + '/' + realname, val)
        ret = { 'element': 'element', 'name': realname, 'child': child }

        if mod:
            return { 'element': mod, 'child': ret }
        else:
            return ret

    def parse_text(self, path, y):
        if None is y or False is y:
            return { 'element': 'empty' }
        if True is not y:
            self._extra_checks.append((path, str(y)))
        return { 'element': 'text' }


def load_rngyaml(source, validate=True):
    source_abr = abbrev(source)
    if is_filepath(source):
        with open(source) as fp:
            y = pyyaml.load(fp)
    else:
        y = pyyaml.load(source)
    assert isinstance(y, dict), \
        "RngYaml {!r} MUST have a mapping at the top-level, but: {}".format(
            source_abr, pprint.pformat(y))

    prefix = y.get('prefix', '$')
    schema = y.get('schema')
    assert isinstance(schema, dict) and 1 == len(schema), (
        "RngYaml {!r} MUST have a //schema element which is a single mapping, but: {}".format(
            source_abr, pprint.pformat(schema)))
    parser = RngYamlParser(prefix)
    ret = parser.parse_pattern('/', schema)

    if validate:
        ret_as_xmlstr = ET.tostring(compile_rngyaml_to_rng(ret), 'unicode')
        rc, err = run_validator(ret_as_xmlstr, relaxng_in_relaxng.DATA)
        assert 0 == rc, err

    return ret


def compile_rngyaml_to_rng(rngyaml):
    assert isinstance(rngyaml, dict), (
        "RngYaml MUST have a mapping at its root, but: {}".format(pprint.pformat(rngyaml)))

    def parse(path, ry, xml):
        if isinstance(ry, dict):
            element = ry['element']
            if 'element' == element:
                name = ry['name']
                sub = ET.SubElement(xml, 'element')
                sub.set('name', name)
                child = ry.get('child')
                if None is not child:
                    parse(path + '/' + 'element:' + name, child, sub)
            elif element in MODIFIERS:
                sub = ET.SubElement(xml, element)
                child = ry['child']
                parse(path + '/' + element, child, sub)
            elif 'text' == element:
                sub = ET.SubElement(xml, element)
        elif isinstance(ry, list):
            for e in ry:
                parse(path, e, xml)
        else:
            raise Exception("{}: what is {}".format(path, pprint.pformat(ry)))
    dummy_root = ET.Element(None)
    parse('/', rngyaml, dummy_root)
    root = next(child for child in dummy_root)
    root.set('xmlns', 'http://relaxng.org/ns/structure/1.0')
    return root


def is_scalar(x):
    '''
    >>> is_scalar('a')
    True
    >>> is_scalar(1)
    True
    >>> is_scalar(0.1)
    True
    >>> is_scalar(2**70)
    True
    >>> is_scalar(True)
    True
    >>> is_scalar({})
    False
    >>> is_scalar([])
    False
    >>> is_scalar(object())
    False
    '''

    return isinstance(x, (str, numbers.Number, bool))


def load_yaml_as_xml(source, attribute_prefix='_'):
    source_abr = source if len(source) <= 13 else source[ :5] + '...' + source[-5: ]
    y = pyyaml.load(source)
    assert isinstance(y, dict), \
        "invalid YAML {!r}: the top-level datatype must be a mapping (got {})".format(
            source_abr, type(y))
    assert 1 == len(y), (
        "invalid YAML {!r}: the top-level mapping must contain a single entry "
        "(got {} entries)".format(source_abr, len(y)))

    k, v = next(p for p in y.items())
    root = ET.Element(str(k))

    def rec_add(path, yaml, xml):
        if isinstance(yaml, dict):
            for k, v in yaml.items():
                if attribute_prefix == k[0:1]:
                    s = str(v)
                    if isinstance(v, bool):
                        s = s.lower()
                    xml.set(k, s)
                else:
                    sub = ET.SubElement(xml, k)
                    rec_add(path + '/' + k, v, sub)
        elif isinstance(yaml, list):
            for e in yaml:
                rec_add(path, e, xml)
        else:
            raise Exception("unexpected structure at {}: {} (of type {})".format(
                path, yaml, type(yaml)))
    rec_add('/', v, root)

    assert validate(ET.tostring(root, 'unicode')), \
        "YAML {!r} yields an invalid XML".format(source_abr)

    return ET.ElementTree(root)


def is_filepath(s):
    '''
    >>> is_filepath('a')
    False
    >>> is_filepath('/xyzzy')
    False
    >>> is_filepath(__file__)
    True
    '''

    assert isinstance(s, str), "invalid input {!r} of type {}".format(s, type(s))
    if os.linesep in s:
        return False
    return os.path.exists(s)


def validate(data, schema=None):
    return 0 == run_validator(data, schema)[0]


def run_validator(data, schema=None):

    def with_temp_file(suf, data, fun):
        with tempfile.NamedTemporaryFile(mode='w', suffix=".{}.xml".format(suf)) as fp:
            path = fp.name
            fp.write(data)
            fp.flush()
            return fun(path)

    def with_prepared_input(source, tmp_sfx, fun):
        if is_filepath(source):
            with open(source) as fp:
                return fun(fp)
        else:
            return with_temp_file(tmp_sfx, source, fun)

    def validate1(schema_path):
        def validate0(data_path):
            cmdline = ['xmllint', '--noout']
            if schema_path:
                cmdline.extend(['--relaxng', schema_path])
            cmdline.append(data_path)
            p = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            return (p.returncode, stderr)

        return with_prepared_input(data, 'data', validate0)

    if None is schema:
        return validate1(schema)
    return with_prepared_input(schema, 'rng', validate1)
