import unittest

from jobBot import Options

class TestCommandLineArguments(unittest.TestCase):
    def setUp(self):
        self.options = Options()

    def test_defaults_options_are_set(self):
        opts, args = self.options.parse()
        self.assertEquals(opts.example, 'example-value')