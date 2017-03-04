import os
import os.path
import tempfile
import subprocess

import yaml


def is_file(s):
    '''
    >>> is_file('a')
    False
    >>> is_file('/xyzzy')
    False
    >>> is_file(__file__)
    True
    '''

    if 1 < len(s.split(os.linesep)):
        return False
    return os.path.exists(s)


def validate(data, schema):
    return 0 == run_validator(data, schema)[0]


def run_validator(data, schema):

    def with_temp_file(suf, data, fun):
        with tempfile.NamedTemporaryFile(mode='w', suffix=".{}.xml".format(suf)) as fp:
            path = fp.name
            fp.write(data)
            fp.flush()
            return fun(path)

    def validate1(schema_path):
        def validate0(data_path):
            p = subprocess.Popen(['xmllint', '--noout', '--relaxng', schema_path, data_path],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            return (p.returncode, stdout, stderr)

        if is_file(data):
            return validate0(data)
        else:
            return with_temp_file('data', data, validate0)

    if is_file(schema):
        return validate1(schema)
    else:
        return with_temp_file('rng', schema, validate1)
