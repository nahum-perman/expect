# Python Expect Library

A minimal assertion library inspired by JavaScript's `expect` (e.g., Chai, Jest) for expressive, readable tests in Python.

## Features
- Assert dictionary includes key, value, or subset
- Assert list includes value
- Negation with `to_not`
- Decorator for asserting raised exceptions with expected messages
- mimic JS expect lib:
    Expect
    expect(value)
    Modifiers
    .not
    .resolves
    .rejects
    Matchers
    .toBe(value)
    .toHaveBeenCalled()
    .toHaveBeenCalledTimes(number)
    .toHaveBeenCalledWith(arg1, arg2, ...)
    .toHaveBeenLastCalledWith(arg1, arg2, ...)
    .toHaveBeenNthCalledWith(nthCall, arg1, arg2, ....)
    .toHaveReturned()
    .toHaveReturnedTimes(number)
    .toHaveReturnedWith(value)
    .toHaveLastReturnedWith(value)
    .toHaveNthReturnedWith(nthCall, value)
    .toHaveLength(number)
    .toHaveProperty(keyPath, value?)
    .toBeCloseTo(number, numDigits?)
    .toBeDefined()
    .toBeFalsy()
    .toBeGreaterThan(number | bigint)
    .toBeGreaterThanOrEqual(number | bigint)
    .toBeLessThan(number | bigint)
    .toBeLessThanOrEqual(number | bigint)
    .toBeInstanceOf(Class)
    .toBeNull()
    .toBeTruthy()
    .toBeUndefined()
    .toBeNaN()
    .toContain(item)
    .toContainEqual(item)
    .toEqual(value)
    .toMatch(regexp | string)
    .toMatchObject(object)
    .toMatchSnapshot(propertyMatchers?, hint?)
    .toMatchInlineSnapshot(propertyMatchers?, inlineSnapshot)
    .toStrictEqual(value)
    .toThrow(error?)
    .toThrowErrorMatchingSnapshot(hint?)
    .toThrowErrorMatchingInlineSnapshot(inlineSnapshot)
    Asymmetric Matchers
    expect.anything()
    expect.any(constructor)
    expect.arrayContaining(array)
    expect.not.arrayContaining(array)
    expect.closeTo(number, numDigits?)
    expect.objectContaining(object)
    expect.not.objectContaining(object)
    expect.stringContaining(string)
    expect.not.stringContaining(string)
    expect.stringMatching(string | regexp)
    expect.not.stringMatching(string | regexp)
    Assertion Count
    expect.assertions(number)
    expect.hasAssertions()
    Extend Utilities
    expect.addEqualityTesters(testers)
    expect.addSnapshotSerializer(serializer)
    expect.extend(matchers)

## Installation
No installation required. Just copy `expect_test.py` into your project.

## Usage Examples

```python
from expect_test import expect

# Dictionary includes subset
expect({'a': 1, 'b': 2}).to.include({'a': 1})

# Dictionary includes key
expect({'a': 1, 'b': 2}).to.include.key('a')

# Dictionary includes value
expect({'a': 1, 'b': 2}).to.include.value(2)

# List includes value
expect(['a', 'b']).to.include('a')

# Negation
expect({'a': 1, 'b': 2}).to_not.include({'c': 3})
expect({'a': 1, 'b': 2}).to_not.include.key('c')
expect({'a': 1, 'b': 2}).to_not.include.value(3)
expect(['a', 'b']).to_not.include('c')

# Deep dictionary inclusion
expect({'dict_a': {'a': 1, 'b': 2}, 'dict_b': {}}).to.include({'dict_a': {'a': 1, 'b': 2}})

# Asserting exceptions (with pytest)
@assert_raises("assert 'c' in dict_keys(['a', 'b'])")
def test_include_key_is_missing():
    expect({'a': 1, 'b': 2}).to.include.key('c')
```

## Requirements
- Python 3.6+
- [pytest](https://pytest.org/) (for running tests and using `assert_raises`)

## License
MIT
