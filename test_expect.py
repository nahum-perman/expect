from expect import expect
import pytest
import re

SIMPLE_DICT = {'a': 1, 'b': 2}

class TestDictIncludesDict(object):
    def test_include_ok(self):
        expect(SIMPLE_DICT).to.include({'b': 2})

    def test_include_different_value(self):
        with pytest.raises(AssertionError, match='assert 3 == 2'):
            expect(SIMPLE_DICT).to.include({'b': 3})

    def test_include_key_missing(self):
        with pytest.raises(AssertionError, match='assert 3 == None'):
            expect(SIMPLE_DICT).to.include({'c': 3})

    def test_not_include(self):
        expect(SIMPLE_DICT).to_not.include({'c' : 3})

    def test_not_include_missing(self):
        with pytest.raises(AssertionError, match='assert 2 != 2'):
            expect(SIMPLE_DICT).to_not.include({'b' : 2})

    def test_include_dict(self):
        expect({'dict_a' : SIMPLE_DICT, 'dict_b': {}}).to.include({'dict_a' : SIMPLE_DICT})

class TestDictIncludesKey(object):
    def test_include_key(self):
        expect(SIMPLE_DICT).to.include.key('a')

    def test_include_key_is_missing(self):
        with pytest.raises(AssertionError, match=re.escape("assert 'c' in ['a', 'b']")):
            expect(SIMPLE_DICT).to.include.key('c')

    def test_not_include_key(self):
        expect(SIMPLE_DICT).to_not.include.key('c')

class TestListIncludesValue(object):
    def test_include_in_list(self):
        expect(['a', 'b']).to.include('a')

    def test_include_in_list_fail(self):
        with pytest.raises(AssertionError, match=re.escape("assert 'c' in ['a', 'b']")):
            expect(['a', 'b']).to.include('c')

class TestDictIncludesValue(object):
    def test_include_in_dict(self):
        expect(SIMPLE_DICT).to.include.value(1)

    def test_include_in_dict_fail(self):
        with pytest.raises(AssertionError, match=re.escape("assert 3 in [1, 2]")):
            expect(SIMPLE_DICT).to.include.value(3)

class TestDictIncludeDeep(object):
    def test_include_dict_in_dict(self):
        # This will fail: deep key search is not implemented
        expect({'dict_a': SIMPLE_DICT, 'dict_b' : {'c' : 3}}).to.include({'a' : 1})

class TestToBe:
    def test_to_be_pass(self):
        a = object()
        expect(a).to.be(a)

    def test_to_be_fail(self):
        with pytest.raises(AssertionError, match="assert <object object at"):
            expect(object()).to.be(object())

class TestToEqual:
    def test_to_equal_pass(self):
        expect([1, 2, 3]).to.equal([1, 2, 3])

    def test_to_equal_fail(self):
        with pytest.raises(AssertionError, match=re.escape("assert [1, 2, 3] == [1, 2, 4]")):
            expect([1, 2, 3]).to.equal([1, 2, 4])

    def test_to_equal_type_mismatch(self):
        with pytest.raises(AssertionError, match=re.escape("assert [1, 2, 3] == (1, 2, 3)")):
            expect([1, 2, 3]).to.equal((1, 2, 3))

class TestToBeInstanceOf:
    def test_to_be_instance_of_pass(self):
        expect(5).to.be_instance_of(int)

    def test_to_be_instance_of_fail(self):
        with pytest.raises(AssertionError, match=re.escape("assert isinstance('hi', int)")):
            expect('hi').to.be_instance_of(int)

    def test_to_be_instance_of_type_mismatch(self):
        with pytest.raises(AssertionError, match=re.escape("assert isinstance([1, 2, 3], dict)")):
            expect([1, 2, 3]).to.be_instance_of(dict)

class TestToBeTruthy:
    def test_to_be_truthy_pass(self):
        expect(1).to.be_truthy()
        expect([1]).to.be_truthy()

    def test_to_be_truthy_fail(self):
        with pytest.raises(AssertionError, match=re.escape("assert bool(0) is True")):
            expect(0).to.be_truthy()

class TestToBeFalsy:
    def test_to_be_falsy_pass(self):
        expect(0).to.be_falsy()
        expect([]).to.be_falsy()

    def test_to_be_falsy_fail(self):
        with pytest.raises(AssertionError, match=re.escape("assert bool(1) is False")):
            expect(1).to.be_falsy()

class TestToBeNull:
    def test_to_be_null_pass(self):
        expect(None).to.be_null()

    def test_to_be_null_fail(self):
        with pytest.raises(AssertionError, match="assert 5 is None"):
            expect(5).to.be_null()

class TestToBeUndefined:
    def test_to_be_undefined_pass(self):
        expect(None).to.be_undefined()

    def test_to_be_undefined_fail(self):
        with pytest.raises(AssertionError, match="assert 5 is None"):
            expect(5).to.be_undefined()

class TestToContain:
    def test_to_contain_pass(self):
        expect([1, 2, 3]).to.contain(2)
        expect('abc').to.contain('b')

    def test_to_contain_fail(self):
        with pytest.raises(AssertionError, match="assert 4 in \\[1, 2, 3\\]"):
            expect([1, 2, 3]).to.contain(4)

    def test_to_contain_type_mismatch(self):
        with pytest.raises(TypeError, match="argument of type 'int' is not iterable"):
            expect(123).to.contain('a')

class TestToHaveLength:
    def test_to_have_length_pass(self):
        expect([1, 2, 3]).to.have_length(3)
        expect('').to.have_length(0)

    def test_to_have_length_fail(self):
        with pytest.raises(AssertionError, match=r"assert len\(\[1, 2, 3\]\) == 2"):
            expect([1, 2, 3]).to.have_length(2)

    def test_to_have_length_type_mismatch(self):
        with pytest.raises(TypeError, match=r"object of type 'int' has no len\(\)"):
            expect(123).to.have_length(3)

class TestToMatch:
    def test_to_match_pass(self):
        expect('hello world').to.match('hello')
        expect('hello world').to.match(r'world$')

    def test_to_match_fail(self):
        with pytest.raises(AssertionError, match=r"assert re.search\('bye', 'hello world'\)"):
            expect('hello world').to.match('bye')

    def test_to_match_type_mismatch(self):
        with pytest.raises(TypeError, match="expected string or bytes-like object, got 'int'"):
            expect(123).to.match('1')

class TestToThrow:
    def test_to_throw_pass(self):
        def raises():
            raise ValueError('fail!')
        expect(raises).to.throw(ValueError)

    def test_to_throw_fail(self):
        def does_not_raise():
            pass
        with pytest.raises(AssertionError, match="assert raised"):
            expect(does_not_raise).to.throw(ValueError)

class TestToBeDefined:
    def test_to_be_defined_pass(self):
        expect(1).to_be_defined()

    def test_to_be_defined_fail(self):
        with pytest.raises(AssertionError, match="assert None is not None"):
            expect(None).to_be_defined()

class TestToBeGreaterThan:
    def test_to_be_greater_than_pass(self):
        expect(5).to_be_greater_than(2)

    def test_to_be_greater_than_fail(self):
        with pytest.raises(AssertionError, match="assert 2 > 5"):
            expect(2).to_be_greater_than(5)

class TestToBeGreaterThanOrEqual:
    def test_to_be_greater_than_or_equal_pass(self):
        expect(5).to_be_greater_than_or_equal(5)
        expect(6).to_be_greater_than_or_equal(5)

    def test_to_be_greater_than_or_equal_fail(self):
        with pytest.raises(AssertionError, match="assert 4 >= 5"):
            expect(4).to_be_greater_than_or_equal(5)

class TestToBeLessThan:
    def test_to_be_less_than_pass(self):
        expect(2).to_be_less_than(5)

    def test_to_be_less_than_fail(self):
        with pytest.raises(AssertionError, match="assert 5 < 2"):
            expect(5).to_be_less_than(2)

class TestToBeLessThanOrEqual:
    def test_to_be_less_than_or_equal_pass(self):
        expect(2).to_be_less_than_or_equal(5)
        expect(5).to_be_less_than_or_equal(5)

    def test_to_be_less_than_or_equal_fail(self):
        with pytest.raises(AssertionError, match="assert 6 <= 5"):
            expect(6).to_be_less_than_or_equal(5)

class TestToHaveProperty:
    def test_to_have_property_dict(self):
        expect({'a': 1}).to_have_property('a')
        expect({'a': 1}).to_have_property('a', 1)

    def test_to_have_property_dict_fail(self):
        with pytest.raises(AssertionError, match="assert b in {'a': 1}"):
            expect({'a': 1}).to_have_property('b')

    def test_to_have_property_object(self):
        class Foo:
            bar = 42
        expect(Foo()).to_have_property('bar')
        expect(Foo()).to_have_property('bar', 42)

    def test_to_have_property_object_fail(self):
        class Foo:
            pass
        with pytest.raises(AssertionError, match="assert hasattr"):
            expect(Foo()).to_have_property('bar')

class TestComplexUseCases:
    def test_nested_dict_property(self):
        data = {'user': {'profile': {'name': 'Alice', 'age': 30}}}
        expect(data['user']['profile']).to_have_property('name', 'Alice')
        expect(data['user']['profile']).to_have_property('age', 30)

    def test_list_of_dicts(self):
        users = [
            {'id': 1, 'name': 'Alice'},
            {'id': 2, 'name': 'Bob'},
        ]
        expect(users).to.contain({'id': 1, 'name': 'Alice'})
        expect(users[1]).to.to_have_property('name', 'Bob')

    def test_combined_matchers(self):
        class Foo:
            bar = [1, 2, 3]
        foo = Foo()
        expect(foo).to_have_property('bar')
        expect(foo.bar).to.have_length(3)
        expect(foo.bar).to.contain(2)

    def test_negation_complex(self):
        data = {'a': 1, 'b': 2}
        expect(data).to_not.to_have_property('c')
        expect([1, 2, 3]).to_not.contain(4)
        expect(None).to_not.be_truthy()

    def test_throw_with_message(self):
        def raises():
            raise ValueError('bad value!')
        try:
            expect(raises).to.throw(ValueError)
        except AssertionError:
            assert False, 'Should not raise AssertionError for correct exception type'
        # Check wrong exception type
        def raises_type():
            raise TypeError('bad type!')
        try:
            expect(raises_type).to.throw(ValueError)
        except AssertionError as e:
            assert 'assert raised exception TypeError is ValueError' in str(e)

class TestToHaveLengthAlias:
    def test_to_have_length_alias(self):
        expect([1, 2, 3]).to_have_length(3)
        expect('abc').to_have_length(3)

class TestToContainAlias:
    def test_to_contain_alias(self):
        expect([1, 2, 3]).to_contain(2)
        expect('abc').to_contain('b')

class TestToBeCloseTo:
    def test_to_be_close_to_pass(self):
        expect(3.1415926).to_be_close_to(3.1415927, 6)

    def test_to_be_close_to_fail(self):
        with pytest.raises(AssertionError):
            expect(3.1415).to_be_close_to(3.14, 4)

class TestToBeNaN:
    def test_to_be_nan_pass(self):
        import math
        expect(float('nan')).to_be_nan()

    def test_to_be_nan_fail(self):
        with pytest.raises(AssertionError):
            expect(1.0).to_be_nan()

class TestToContainEqual:
    def test_to_contain_equal_pass(self):
        expect([{'a': 1}, {'b': 2}]).to_contain_equal({'a': 1})

    def test_to_contain_equal_fail(self):
        with pytest.raises(AssertionError, match="assert some element equal to {'c': 3} in "):
            expect([{'a': 1}, {'b': 2}]).to_contain_equal({'c': 3})

class TestToMatchObject:
    def test_to_match_object_pass(self):
        expect({'a': 1, 'b': 2}).to_match_object({'a': 1})

    def test_to_match_object_fail(self):
        with pytest.raises(AssertionError, match="assert a: 2 in {'a': 1, 'b': 2}"):
            expect({'a': 1, 'b': 2}).to_match_object({'a': 2})

class TestToBeAliases:
    def test_to_be_truthy_alias(self):
        expect(1).to_be_truthy()
    def test_to_be_falsy_alias(self):
        expect(0).to_be_falsy()
    def test_to_be_null_alias(self):
        expect(None).to_be_null()
    def test_to_be_undefined_alias(self):
        expect(None).to_be_undefined()
    def test_to_be_instance_of_alias(self):
        expect(1).to_be_instance_of(int)
    def test_to_equal_alias(self):
        expect([1]).to_equal([1])
    def test_to_be_alias(self):
        a = object()
        expect(a).to_be(a)

class TestToStrictEqual:
    def test_to_strict_equal_pass(self):
        expect([1, 2, 3]).to_strict_equal([1, 2, 3])
        expect({'a': 1}).to_strict_equal({'a': 1})

    def test_to_strict_equal_fail(self):
        with pytest.raises(AssertionError, match=re.escape("assert [1, 2, 3] is strictly equal to (1, 2, 3)")):
            expect([1, 2, 3]).to_strict_equal((1, 2, 3))
        with pytest.raises(AssertionError, match=re.escape("assert {'a': 1} is strictly equal to {'a': 2}")):
            expect({'a': 1}).to_strict_equal({'a': 2})

class TestToThrowAlias:
    def test_to_throw_alias(self):
        def raises():
            raise ValueError('fail!')
        expect(raises).to_throw(ValueError)

class TestToMatchAlias:
    def test_to_match_alias(self):
        expect('hello world').to_match('hello')

class TestToContainEqualAlias:
    def test_to_contain_equal_alias(self):
        expect([{'a': 1}, {'b': 2}]).to_contain_equal({'a': 1})

class TestToMatchObjectAlias:
    def test_to_match_object_alias(self):
        expect({'a': 1, 'b': 2}).to_match_object({'a': 1})

class TestSnapshotPlaceholders:
    def test_to_match_snapshot_not_implemented(self):
        with pytest.raises(NotImplementedError):
            expect(1).to_match_snapshot()
    def test_to_match_inline_snapshot_not_implemented(self):
        with pytest.raises(NotImplementedError):
            expect(1).to_match_inline_snapshot()
    def test_to_throw_error_matching_snapshot_not_implemented(self):
        with pytest.raises(NotImplementedError):
            expect(lambda: 1).to_throw_error_matching_snapshot()
    def test_to_throw_error_matching_inline_snapshot_not_implemented(self):
        with pytest.raises(NotImplementedError):
            expect(lambda: 1).to_throw_error_matching_inline_snapshot()
