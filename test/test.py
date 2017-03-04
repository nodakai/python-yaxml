import unittest

import yaxml


class Test(unittest.TestCase):
    def test_validate(self):
        assert yaxml.validate(
            '<foo/>',
            '''
<element name="foo" xmlns="http://relaxng.org/ns/structure/1.0" >
    <empty/>
</element>
            ''')

        assert yaxml.validate(yaxml.relaxng_in_relaxng.DATA, yaxml.relaxng_in_relaxng.DATA)
