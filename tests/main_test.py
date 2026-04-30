class NestedTest:
    class BuiltInFunctionTest:
        """THis is a dummy test, we don't usually test built-ins"""

        def test_len(self):
            assert len([1, 2, 3]) == 3

    class DummyTest:
        def test_addition(self):
            assert 1 + 2 == 3

        def test_subtraction(self):
            assert 3 - 1 == 2
