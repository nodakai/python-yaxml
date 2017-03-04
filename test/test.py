import unittest

import yaxml


class Test(unittest.TestCase):
    def test_is_file(self):
        assert not yaxml.is_file('a')
        assert not yaxml.is_file('/xyzzy')
        assert yaxml.is_file('/etc/hosts')

    def test1(self):
        pass
