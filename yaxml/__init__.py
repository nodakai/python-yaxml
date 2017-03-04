import os
import os.path
import tempfile
import subprocess

import yaml


def is_file(s):
    if 1 < len(s.split(os.linesep)):
        return False
    return os.path.exists(s)


def validate(data, schema):

    def validate1(schema_path):
        def validate0(data_path):
            p = subprocess.Popen(['xmllint', '--relaxng', schema_path, data_path])
            stdout, stderr = p.communicate()
            return (p.returncode, stdout, stderr)

        if is_file(data):
            return validate0(data)
        else:
            with tempfile.NamedTemporaryFile(suffix='.xml') as data_file:
                data_path = data_file.name
                data_file.write(data)
                return validate0(data_path)

    if is_file(schema):
        return validate1(schema)
    else:
        with tempfile.NamedTemporaryFile(suffix='.xml') as schema_file:
            schema_path = schema_file.name
            schema_file.write(schema)
            return validate1(schema_path)
