import pytest
from tfchain.encoders import encoder_sia_get
from tfchain.encoders.exceptions import IntegerOutOfRange, SliceLengthOutOfRange


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
