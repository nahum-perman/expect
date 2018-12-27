import pytest

def assert_raises(expected_message):
    def _assert_raises(func):
        def assert_raises_decorator(*args):
            with pytest.raises(AssertionError) as ex:
                func(*args)
            assert expected_message in str(ex)

        return assert_raises_decorator
    return _assert_raises

SIMPLE_DICT = {'a': 1, 'b': 2}

class TestDictIncludesDict(object):
    def test_include_ok(self):
        expect(SIMPLE_DICT).to.include({'b': 2})

    @assert_raises('assert 3 == 2')
    def test_include_different_value(self):
        expect(SIMPLE_DICT).to.include({'b': 3})

    @assert_raises('assert 3 == None')
    def test_include_key_missing(self):
        expect(SIMPLE_DICT).to.include({'c': 3})

    def test_not_include(self):
        expect(SIMPLE_DICT).to_not.include({'c' : 3})

class TestDictIncludesKey(object):
    def test_include_key(self):
        expect(SIMPLE_DICT).to.include.key('a')

    @assert_raises("assert 'c' in ['a', 'b']")
    def test_include_key_is_missing(self):
        expect(SIMPLE_DICT).to.include.key('c')

    def test_not_include_key(self):
        expect(SIMPLE_DICT).to_not.include.key('c')

class TestListIncludesValue(object):
    def test_include_in_list(self):
        expect(['a', 'b']).to.include('a')

    @assert_raises("assert 'c' in ['a', 'b']")
    def test_include_in_list_fail(self):
        expect(['a', 'b']).to.include('c')

class expect:
    def __init__(self, actual):
        self._actual = actual
        self._flags = []
        self.include = expect.include_class(self)

    def is_negate(self):
        return 'negate' in self._flags

    @property
    def to(self):
        return self

    @property
    def to_not(self):
        self._flags.append('negate')
        return self

    class include_class:
        def __init__(self, expected):
            self.expected = expected

        def key(self, key):
            self.expected.include_key(key)

        def __call__(self, subset):
            self.expected.include_subset(subset)


    def include_subset(expected, subset):
        for key in subset:
            if expected.is_negate():
                assert(subset[key] != expected._actual.get(key))
            else:
                if isinstance(subset, str):
                    assert(subset in expected._actual)
                else:
                    assert(subset[key] == expected._actual.get(key))


    def include_key(self, key):
        assert(type(self._actual) == type({}))

        if self.is_negate():
            assert(key not in self._actual.keys())
        else :
            assert(key in self._actual.keys())
