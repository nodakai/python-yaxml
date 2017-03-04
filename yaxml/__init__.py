import os
import os.path
import tempfile
import subprocess
import numbers
import xml.etree.ElementTree as ET

import yaml as pyyaml

from . import relaxng_in_relaxng


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
    source_human = source if len(source) <= 13 else source[ :5] + '...' + source[-5: ]
    y = pyyaml.load(source)
    assert isinstance(y, dict), \
        "invalid YAML {!r}: the top-level datatype must be a mapping (got {})".format(
            source_human, type(y))
    assert 1 == len(y), (
        "invalid YAML {!r}: the top-level mapping must contain a single entry "
        "(got {} entries)".format(source_human, len(y)))

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
        "YAML {!r} yields an invalid XML".format(source_human)

    return ET.ElementTree(root)


def is_file(s):
    '''
    >>> is_file('a')
    False
    >>> is_file('/xyzzy')
    False
    >>> is_file(__file__)
    True
    '''

    assert isinstance(s, str), type(s)
    if 1 < len(s.split(os.linesep)):
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

    def validate1(schema_path):
        def validate0(data_path):
            cmdline = ['xmllint', '--noout']
            if schema_path:
                cmdline.extend(['--relaxng', schema_path])
            cmdline.append(data_path)
            p = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            return (p.returncode, stdout, stderr)

        if is_file(data):
            return validate0(data)
        else:
            return with_temp_file('data', data, validate0)

    if None is schema or is_file(schema):
        return validate1(schema)
    else:
        return with_temp_file('rng', schema, validate1)
