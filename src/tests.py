#!/usr/bin/env python

'''\
$ env TEST=yes python tests.py
'''

from tlsarchiverfront import app


class FlaskApplicationTestCase(unittest.TestCase):
    def setUp(self):
        if not app.testing:
            raise Exception("Ensure shell environment variable TEST=yes is set before running tests.")
        self.app = app.test_client()

    def test_something(self):
        self.assertTrue(True)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
