import pytest
from tfchain.encoders import encoder_rivine_get, encoder_sia_get
from tfchain.encoders.exceptions import IntegerOutOfRange, SliceLengthOutOfRange
from tfchain.encoders import BaseRivineObjectEncoder, BaseSiaObjectEncoder


def test_rivine_basic_encoding():
    e = encoder_rivine_get()

    # you can add integers, booleans, iterateble objects, strings,
    # bytes and byte arrays. Dictionaries and objects are not supported.
    e.add(False)
    e.add("a")
    e.add([1, True, "foo"])
    e.add(b"123")

    # the result is a single bytearray
    assert e.data == b'\x00\x02a\x06\x01\x00\x00\x00\x00\x00\x00\x00\x01\x06foo\x06123'


def test_sia_basic_encoding():
    e = encoder_sia_get()

    # you can add integers, booleans, iterateble objects, strings,
    # bytes and byte arrays. Dictionaries and objects are not supported.
    e.add(False)
    e.add("a")
    e.add([1, True, "foo"])
    e.add(b"123")

    # the result is a single bytearray
    assert e.data == b'\x00\x01\x00\x00\x00\x00\x00\x00\x00a\x03\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x03\x00\x00\x00\x00\x00\x00\x00foo\x03\x00\x00\x00\x00\x00\x00\x00123'


def test_rivine_types():
    e = encoder_rivine_get()

    # in the rivine_basic test we saw we can
    # serialise anything using the add method.
    # One can however also directly encode the specific type as desired,
    # which allows for example the encoding of an integer as a specific byte size.
    e.add_int8(1)
    e.add_int16(2)
    e.add_int24(3)
    e.add_int32(4)
    e.add_int64(5)

    # a single byte can be added as well
    e.add_byte(6)
    e.add_byte('4')
    e.add_byte(b'2')

    # array are like slices, but have no length prefix,
    # therefore this is only useful if there is a fixed amount of elements,
    # known by all parties
    e.add_array([False, True, True])

    # the result is a single bytearray
    assert e.data == b'\x01\x02\x00\x03\x00\x00\x04\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x0642\x00\x01\x01'


def test_sia_types():

    e = encoder_sia_get()

    # in the sia_basic test we saw we can
    # serialise anything using the add method.

    # by default strings, byte arrays and iterateable objects
    # are encoded as slices.
    #
    # array are like slices, but have no length prefix,
    # therefore this is only useful if there is a fixed amount of elements,
    # known by all parties
    e.add_array([False, True, True])

    # a single byte can be added as well
    e.add_byte(6)
    e.add_byte('4')
    e.add_byte(b'2')

    # the result is a single bytearray
    assert e.data == b'\x00\x01\x01\x0642'


def test_rivine_custom():
    e = encoder_rivine_get()

    # a class that provides a custom encoding logic for its types,
    # required in order to be able to encode Python objects
    class Answer(BaseRivineObjectEncoder):
        def __init__(self, number=0):
            self._number = number

        def rivine_binary_encode(self, encoder):
            if self._number % 2 != 0:
                return encoder.add_int24(self._number - 1)
            return encoder.add_int24(self._number)

    # when we add our objects they will be encoded
    # using the method as provided by its type
    e.add(Answer())
    e.add(Answer(43))

    # this works for slices and arrays as well
    e.add_array([Answer(5), Answer(2)])

    # the result is a single bytearray
    assert e.data == b'\x00\x00\x00\x2A\x00\x00\x04\x00\x00\x02\x00\x00'


def test_sia_custom():
    e = encoder_sia_get()

    # a class that provides a custom encoding logic for its types,
    # required in order to be able to encode Python objects
    class Answer(BaseSiaObjectEncoder):
        def __init__(self, number=0):
            self._number = number

        def sia_binary_encode(self, encoder):
            if self._number == 42:
                return encoder.add(True)
            return encoder.add(False)

    # when we add our objects they will be encoded
    # using the method as provided by its type
    e.add(Answer())
    e.add(Answer(42))

    # this works for slices and arrays as well
    e.add_array([Answer(5), Answer(2)])

    # the result is a single bytearray
    assert e.data == b'\x00\x01\x00\x00'


def test_rivine_limits():
    e = encoder_rivine_get()

    # everything has limits, so do types,
    # that is what this test is about

    # no integer can be negative
    with pytest.raises(IntegerOutOfRange):
        e.add(-1)
    with pytest.raises(IntegerOutOfRange):
        e.add_int64(-1)
    with pytest.raises(IntegerOutOfRange):
        e.add_int32(-1)
    with pytest.raises(IntegerOutOfRange):
        e.add_int24(-1)
    with pytest.raises(IntegerOutOfRange):
        e.add_int16(-1)
    with pytest.raises(IntegerOutOfRange):
        e.add_int8(-1)

    # integers have upper limits as well
    with pytest.raises(IntegerOutOfRange):
        e.add(1 << 64)
    with pytest.raises(IntegerOutOfRange):
        e.add_int64(1 << 64)
    with pytest.raises(IntegerOutOfRange):
        e.add_int32(1 << 32)
    with pytest.raises(IntegerOutOfRange):
        e.add_int24(1 << 24)
    with pytest.raises(IntegerOutOfRange):
        e.add_int16(1 << 16)
    with pytest.raises(IntegerOutOfRange):
        e.add_int8(1 << 8)

    # slices have limits too,
    # but should you ever user (1<<29) or more objects,
    # you have other things to worry about


def test_sia_custom():
    e = encoder_sia_get()

    # everything has limits, so do types,
    # that is what this test is about

    # no integer can be negative
    with pytest.raises(IntegerOutOfRange):
        e.add(-1)
    # integers have an upper bound
    with pytest.raises(IntegerOutOfRange):
        e.add(1 << 64)
