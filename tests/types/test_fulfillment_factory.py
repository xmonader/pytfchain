
from tfchain.types.BaseDataType import BaseDataTypeClass
from tfchain.types.CryptoTypes import PublicKey
from tfchain.types.PrimitiveTypes import BinaryData, Hash
from tfchain.types.ConditionTypes import UnlockHash, UnlockHashType, ConditionNil, \
    ConditionUnlockHash, ConditionAtomicSwap, ConditionMultiSignature, AtomicSwapSecret
from tfchain.types.FulfillmentTypes import FulfillmentFactory
from tfchain.encoders import encoder_rivine_get, encoder_sia_get


def test_fulfillments():
    # some util test methods
    factory = FulfillmentFactory()

    def test_encoded(encoder, obj, expected):
        encoder.add(obj)
        output = encoder.data.hex()
        if expected != output:
            msg = "{} != {}".format(expected, output)
            raise Exception("unexpected encoding result: " + msg)

    def test_sia_encoded(obj, expected):
        test_encoded(encoder_sia_get(), obj, expected)

    def test_rivine_encoded(obj, expected):
        test_encoded(encoder_rivine_get(), obj, expected)

    # single signature fulfillments are supported
    ss_json = {"type": 1, "data": {"publickey": "ed25519:dda39750fff2d869badc797aaad1dea8c6bcf943879421c58ac8d8e2072d5b5f",
                                   "signature": "818dfccee2cb7dbe4156169f8e1c5be49a3f6d83a4ace310863d7b3b698748e3e4d12522fc1921d5eccdc108b36c84d769a9cf301e969bb05db1de9295820300"}}
    ssf = factory.from_json(ss_json)
    assert ssf.json() == ss_json
    test_sia_encoded(ssf, '018000000000000000656432353531390000000000000000002000000000000000dda39750fff2d869badc797aaad1dea8c6bcf943879421c58ac8d8e2072d5b5f4000000000000000818dfccee2cb7dbe4156169f8e1c5be49a3f6d83a4ace310863d7b3b698748e3e4d12522fc1921d5eccdc108b36c84d769a9cf301e969bb05db1de9295820300')
    test_rivine_encoded(ssf, '01c401dda39750fff2d869badc797aaad1dea8c6bcf943879421c58ac8d8e2072d5b5f80818dfccee2cb7dbe4156169f8e1c5be49a3f6d83a4ace310863d7b3b698748e3e4d12522fc1921d5eccdc108b36c84d769a9cf301e969bb05db1de9295820300')
    assert ssf.is_fulfilled(ConditionUnlockHash())

    # atomic swap fulfillments are supported
    as_json = {"type": 2, "data": {"publickey": "ed25519:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                                   "signature": "abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefab", "secret": "def789def789def789def789def789dedef789def789def789def789def789de"}}
    asf = factory.from_json(as_json)
    assert asf.json() == as_json
    test_sia_encoded(asf, '02a000000000000000656432353531390000000000000000002000000000000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff4000000000000000abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabdef789def789def789def789def789dedef789def789def789def789def789de')
    test_rivine_encoded(asf, '02090201ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabdef789def789def789def789def789dedef789def789def789def789def789de')
    assert asf.is_fulfilled(ConditionAtomicSwap())
    # atomic swap fulfillments without secrets are supported
    as_json = {"type": 2, "data": {"publickey": "ed25519:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                                   "signature": "abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefab"}}
    asf = factory.from_json(as_json)
    assert asf.json() == as_json
    test_sia_encoded(asf, '028000000000000000656432353531390000000000000000002000000000000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff4000000000000000abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefab')
    test_rivine_encoded(asf, '02c401ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefab')
    assert asf.is_fulfilled(ConditionAtomicSwap())

    # multi signature fulfillments are supported
    ms_json = {"type": 3, "data": {"pairs": [{"publickey": "ed25519:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "signature": "abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefab"}, {
        "publickey": "ed25519:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "signature": "abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefab"}]}}
    msf = factory.from_json(ms_json)
    assert msf.json() == ms_json
    test_sia_encoded(msf, '0308010000000000000200000000000000656432353531390000000000000000002000000000000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff4000000000000000abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefab656432353531390000000000000000002000000000000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff4000000000000000abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefab')
    test_rivine_encoded(msf, '0315030401ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefab01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefab')
    assert msf.is_fulfilled(ConditionMultiSignature(min_nr_sig=1))
    assert msf.is_fulfilled(ConditionMultiSignature(min_nr_sig=2))
