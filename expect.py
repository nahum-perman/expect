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

        def value(self, value):
            self.expected.include_value(value)

        def __call__(self, subset):
            self.expected.include_subset(subset)

    def include_subset(expected, subset):
        def deep_search(d, key):
            if isinstance(d, dict):
                if key in d:
                    return d[key]
                for v in d.values():
                    found = deep_search(v, key)
                    if found is not None:
                        return found
            elif isinstance(d, list):
                for item in d:
                    found = deep_search(item, key)
                    if found is not None:
                        return found
            return None

        # If subset is not a dict, treat as value inclusion (for lists, etc.)
        if not isinstance(subset, dict):
            if expected.is_negate():
                assert subset not in expected._actual, f"assert {repr(subset)} not in {repr(expected._actual)}"
            else:
                assert subset in expected._actual, f"assert {repr(subset)} in {repr(expected._actual)}"
            return

        for key in subset:
            if expected.is_negate():
                actual_value = deep_search(expected._actual, key)
                assert subset[key] != actual_value, f"assert {subset[key]} != {actual_value}"
            else:
                actual_value = deep_search(expected._actual, key)
                assert subset[key] == actual_value, f"assert {subset[key]} == {actual_value}"

    def include_key(self, key):
        assert type(self._actual) == type({}), f"assert type({self._actual}) == dict"

        if self.is_negate():
            assert key not in self._actual.keys(), f"assert '{key}' not in {list(self._actual.keys())}"
        else:
            assert key in self._actual.keys(), f"assert '{key}' in {list(self._actual.keys())}"

    def include_value(self, value):
        if self.is_negate():
            assert value not in self._actual.values(), f"assert {value} not in {list(self._actual.values())}"
        else:
            assert value in self._actual.values(), f"assert {value} in {list(self._actual.values())}"

    def be(self, expected):
        if self.is_negate():
            assert self._actual is not expected, f"assert {self._actual} is not {expected}"
        else:
            assert self._actual is expected, f"assert {self._actual} is {expected}"
        return self

    def equal(self, expected):
        if self.is_negate():
            assert self._actual != expected, f"assert {self._actual} != {expected}"
        else:
            assert self._actual == expected, f"assert {self._actual} == {expected}"
        return self

    def be_instance_of(self, cls):
        if self.is_negate():
            assert not isinstance(self._actual, cls), f"assert not isinstance({repr(self._actual)}, {cls.__name__})"
        else:
            assert isinstance(self._actual, cls), f"assert isinstance({repr(self._actual)}, {cls.__name__})"
        return self

    def be_truthy(self):
        if self.is_negate():
            assert not bool(self._actual) is True, f"assert bool({repr(self._actual)}) is not True"
        else:
            assert bool(self._actual) is True, f"assert bool({repr(self._actual)}) is True"
        return self

    def be_falsy(self):
        if self.is_negate():
            assert not bool(self._actual) is False, f"assert bool({repr(self._actual)}) is not False"
        else:
            assert bool(self._actual) is False, f"assert bool({repr(self._actual)}) is False"
        return self

    def be_null(self):
        if self.is_negate():
            assert self._actual is not None, f"assert {self._actual} is not None"
        else:
            assert self._actual is None, f"assert {self._actual} is None"
        return self

    def be_undefined(self):
        # In Python, undefined is best represented as None
        if self.is_negate():
            assert self._actual is not None, f"assert {self._actual} is not None"
        else:
            assert self._actual is None, f"assert {self._actual} is None"
        return self

    def contain(self, item):
        if self.is_negate():
            assert item not in self._actual, f"assert {repr(item)} not in {repr(self._actual)}"
        else:
            assert item in self._actual, f"assert {repr(item)} in {repr(self._actual)}"
        return self

    def have_length(self, length):
        if self.is_negate():
            assert len(self._actual) != length, f"assert len({repr(self._actual)}) != {length}"
        else:
            assert len(self._actual) == length, f"assert len({repr(self._actual)}) == {length}"
        return self

    def match(self, pattern):
        import re
        if self.is_negate():
            assert not re.search(pattern, self._actual), f"assert not re.search({repr(pattern)}, {repr(self._actual)})"
        else:
            assert re.search(pattern, self._actual), f"assert re.search({repr(pattern)}, {repr(self._actual)})"
        return self

    def throw(self, error_type):
        raised = False
        try:
            self._actual()
        except Exception as e:
            raised = True
            assert isinstance(e, error_type), f"assert raised exception {type(e).__name__} is {error_type.__name__}"
        if not raised:
            assert False, "assert raised"
        return self

    def to_be_defined(self):
        if self.is_negate():
            assert self._actual is None, f"assert {self._actual} is None (negated defined)"
        else:
            assert self._actual is not None, f"assert {self._actual} is not None"
        return self

    def to_be_greater_than(self, value):
        if self.is_negate():
            assert not self._actual > value, f"assert {self._actual} <= {value}"
        else:
            assert self._actual > value, f"assert {self._actual} > {value}"
        return self

    def to_be_greater_than_or_equal(self, value):
        if self.is_negate():
            assert not self._actual >= value, f"assert {self._actual} < {value}"
        else:
            assert self._actual >= value, f"assert {self._actual} >= {value}"
        return self

    def to_be_less_than(self, value):
        if self.is_negate():
            assert not self._actual < value, f"assert {self._actual} >= {value}"
        else:
            assert self._actual < value, f"assert {self._actual} < {value}"
        return self

    def to_be_less_than_or_equal(self, value):
        if self.is_negate():
            assert not self._actual <= value, f"assert {self._actual} > {value}"
        else:
            assert self._actual <= value, f"assert {self._actual} <= {value}"
        return self

    def to_have_property(self, key, value=None):
        if self.is_negate():
            assert not (hasattr(self._actual, key) or (isinstance(self._actual, dict) and key in self._actual)), f"assert not hasattr({self._actual}, {key}) or {key} in dict"
        else:
            if isinstance(self._actual, dict):
                assert key in self._actual, f"assert {key} in {self._actual}"
                if value is not None:
                    assert self._actual[key] == value, f"assert {self._actual}[{key}] == {value}"
            else:
                assert hasattr(self._actual, key), f"assert hasattr({self._actual}, {key})"
                if value is not None:
                    assert getattr(self._actual, key) == value, f"assert getattr({self._actual}, {key}) == {value}"
        return self

    def to_have_length(self, length):
        # Alias for have_length
        return self.have_length(length)

    def to_contain(self, item):
        # Alias for contain
        return self.contain(item)

    def to_be_close_to(self, number, num_digits=7):
        if self.is_negate():
            assert not round(self._actual - number, num_digits) == 0, f"assert {self._actual} not close to {number} with {num_digits} digits"
        else:
            assert round(self._actual - number, num_digits) == 0, f"assert {self._actual} close to {number} with {num_digits} digits"
        return self

    def to_be_nan(self):
        import math
        if self.is_negate():
            assert not math.isnan(self._actual), f"assert not math.isnan({self._actual})"
        else:
            assert math.isnan(self._actual), f"assert math.isnan({self._actual})"
        return self

    def to_contain_equal(self, item):
        # Checks if any element in self._actual == item
        if self.is_negate():
            assert not any(x == item for x in self._actual), f"assert no element equal to {item} in {self._actual}"
        else:
            assert any(x == item for x in self._actual), f"assert some element equal to {item} in {self._actual}"
        return self

    def to_match_object(self, obj):
        # Checks if all keys/values in obj are in self._actual (shallow)
        if self.is_negate():
            for k, v in obj.items():
                assert k not in self._actual or self._actual[k] != v, f"assert {k}: {v} not in {self._actual}"
        else:
            for k, v in obj.items():
                assert k in self._actual and self._actual[k] == v, f"assert {k}: {v} in {self._actual}"
        return self

    def to_strict_equal(self, expected):
        # In Python, strict equality is the same as == for most types, but for dicts/lists, check type and value
        if self.is_negate():
            assert type(self._actual) != type(expected) or self._actual != expected, f"assert {self._actual} is not strictly equal to {expected}"
        else:
            assert type(self._actual) == type(expected) and self._actual == expected, f"assert {self._actual} is strictly equal to {expected}"
        return self

    def to_throw(self, error_type):
        return self.throw(error_type)

    def to_match(self, pattern):
        return self.match(pattern)

    # Placeholders for snapshot and advanced matchers (not implemented)
    def to_match_snapshot(self, *args, **kwargs):
        raise NotImplementedError("Snapshot testing is not implemented.")

    def to_match_inline_snapshot(self, *args, **kwargs):
        raise NotImplementedError("Inline snapshot testing is not implemented.")

    def to_throw_error_matching_snapshot(self, *args, **kwargs):
        raise NotImplementedError("Error snapshot testing is not implemented.")

    def to_throw_error_matching_inline_snapshot(self, *args, **kwargs):
        raise NotImplementedError("Inline error snapshot testing is not implemented.")

    def to_be_truthy(self):
        return self.be_truthy()

    def to_be_falsy(self):
        return self.be_falsy()

    def to_be_null(self):
        return self.be_null()

    def to_be_undefined(self):
        return self.be_undefined()

    def to_be_instance_of(self, cls):
        return self.be_instance_of(cls)

    def to_equal(self, expected):
        return self.equal(expected)

    def to_be(self, expected):
        return self.be(expected)
