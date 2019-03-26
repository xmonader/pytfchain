from tfchain.encoders import encoder_rivine_get


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
